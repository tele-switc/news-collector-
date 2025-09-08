# -*- coding: utf-8 -*-
import os, sys, time
from datetime import datetime, timezone
import feedparser
from dateutil import parser as dtparser
from scripts.config import SOURCES, START_DATE_ISO
from scripts.utils import (
    HEADERS, load_dedup, save_dedup, add_item_if_new, make_item, to_iso,
    extract_meta, update_index_indexfile, domain_of, load_gifts
)
from connectors.diffbot import extract_with_diffbot

MAX_META_FETCHES = int(os.getenv("MAX_META_FETCHES", "200"))

def entry_time(e):
    for k in ("published","updated","created"):
        if k in e:
            try: return to_iso(e[k])
            except Exception: pass
    for k in ("published_parsed","updated_parsed"):
        if getattr(e,k,None):
            dt = getattr(e,k)
            try: return to_iso(datetime(*dt[:6], tzinfo=timezone.utc))
            except Exception: pass
    return to_iso(datetime.now(timezone.utc))

def fulltext_allowed(url: str) -> bool:
    wl = os.getenv("FULLTEXT_WHITELIST", "").strip()
    if not wl: return False
    allow = set([d.strip().lower() for d in wl.split(",") if d.strip()])
    d = domain_of(url)
    # 子域也匹配主域
    return any(d == a or d.endswith("." + a) for a in allow)

def try_fill_fulltext(item):
    # 仅当在白名单且有 Diffbot Token 才尝试
    if not fulltext_allowed(item["url"]): 
        return item
    token = os.getenv("DIFFBOT_TOKEN", "").strip()
    if not token:
        return item
    try:
        data = extract_with_diffbot(item["url"], token)
        if not data:
            return item
        # 更新基础元数据（若缺失）
        if data.get("title"): item["title"] = item["title"] or data["title"]
        if data.get("author"): item["author"] = item["author"] or data["author"]
        if data.get("published_at"): item["published_at"] = data["published_at"]
        if data.get("updated_at"): item["updated_at"] = data["updated_at"]
        # 填入全文
        item["content_text"] = data.get("content_text") or ""
        item["content_html"] = data.get("content_html") or ""
        if item["content_text"] or item["content_html"]:
            item["can_publish_fulltext"] = True
    except Exception as e:
        print(f"Diffbot failed: {e}")
    return item

def main():
    start_iso = START_DATE_ISO + "T00:00:00Z"
    dedup = load_dedup()
    gifts = load_gifts()
    added, meta_used = 0, 0

    for key, conf in SOURCES.items():
        for rss in conf.get("rss", []):
            print(f"[{conf['display_name']}] RSS: {rss}")
            feed = feedparser.parse(rss, request_headers=HEADERS)
            for e in getattr(feed, "entries", []):
                url = e.get("link") or e.get("id")
                if not url: continue
                published_iso = entry_time(e)
                if published_iso < start_iso: continue

                title = (e.get("title") or "").strip()
                summary = (e.get("summary") or e.get("description") or "").strip()
                author = (e.get("author") or "").strip()
                updated_at = ""

                # 用网页元数据补齐作者/时间/更严谨标题（不抓正文）
                if (not author or not title):
                    if meta_used < MAX_META_FETCHES:
                        meta = extract_meta(url)
                        if meta.get("author") and not author: author = meta["author"]
                        if meta.get("title") and not title: title = meta["title"]
                        if meta.get("published_at"): published_iso = meta["published_at"]
                        if meta.get("updated_at"): updated_at = meta["updated_at"]
                        meta_used += 1
                        time.sleep(0.3)

                item = make_item(url, title, conf["display_name"], published_iso, summary, author, updated_at)
                # gift 链接（手工维护 docs/gifts.json，key 为 item.id）
                if item["id"] in gifts:
                    item["gift_url"] = gifts[item["id"]]

                # 在白名单/授权范围内，尝试全文
                item = try_fill_fulltext(item)

                if add_item_if_new(dedup, item): added += 1
            time.sleep(0.6)

    save_dedup(dedup)
    update_index_indexfile()
    print(f"Done. New items added: {added}, meta fetches: {meta_used}")
    return 0

if __name__ == "__main__":
    sys.exit(main())

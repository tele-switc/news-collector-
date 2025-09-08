# -*- coding: utf-8 -*-
import requests
from datetime import datetime, timezone
from dateutil import parser as dtparser

HEADERS = {
    "User-Agent": "NewsPortalBot/1.0 (+https://github.com/) requests",
    "Accept": "application/json",
}

def to_iso(dt):
    if not dt: return ""
    if isinstance(dt, str):
        try:
            d = dtparser.parse(dt)
        except Exception:
            return ""
    else:
        d = dt
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    return d.astimezone(timezone.utc).isoformat()

def extract_with_diffbot(url: str, token: str, timeout: int = 45):
    """
    使用 Diffbot Article API 提取合法授权的正文/作者/时间等元数据。
    仅在你有相应授权且站点许可再展示时，在前端显示全文。
    """
    api = "https://api.diffbot.com/v3/article"
    params = {"token": token, "url": url}
    r = requests.get(api, params=params, headers=HEADERS, timeout=timeout)
    r.raise_for_status()
    data = r.json()
    objs = data.get("objects") or []
    if not objs:
        return {}
    o = objs[0]
    authors = []
    if isinstance(o.get("author"), str):
        authors = [o.get("author")]
    if isinstance(o.get("authors"), list):
        authors = [a.get("name") if isinstance(a, dict) else str(a) for a in o["authors"] if a]
    author = ", ".join([a for a in authors if a])

    return {
        "title": o.get("title") or "",
        "author": author or "",
        "published_at": to_iso(o.get("date") or o.get("dateCreated")),
        "updated_at": to_iso(o.get("dateModified")),
        "content_text": o.get("text") or "",
        "content_html": o.get("html") or "",
    }

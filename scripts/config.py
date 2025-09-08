# -*- coding: utf-8 -*-
# 来源清单：RSS 为每日增量，Sitemap 为回填。可按需增删。
SOURCES = {
    "wired": {
        "display_name": "WIRED",
        "domain": "wired.com",
        "rss": ["https://www.wired.com/feed/rss"],
        "sitemap": "https://www.wired.com/sitemap.xml",
    },
    "economist": {
        "display_name": "The Economist",
        "domain": "economist.com",
        "rss": [
            "https://www.economist.com/latest/rss.xml",
            "https://www.economist.com/finance-and-economics/rss.xml",
            "https://www.economist.com/business/rss.xml",
            "https://www.economist.com/international/rss.xml",
            "https://www.economist.com/science-and-technology/rss.xml",
            "https://www.economist.com/culture/rss.xml",
            "https://www.economist.com/europe/rss.xml",
        ],
        "sitemap": "https://www.economist.com/sitemap.xml",
    },
    "scientific_american": {
        "display_name": "Scientific American",
        "domain": "scientificamerican.com",
        "rss": ["https://www.scientificamerican.com/feed/"],
        "sitemap": "https://www.scientificamerican.com/sitemap.xml",
    },
    "the_atlantic": {
        "display_name": "The Atlantic",
        "domain": "theatlantic.com",
        "rss": ["https://www.theatlantic.com/feed/all/"],
        "sitemap": "https://www.theatlantic.com/sitemap.xml",
    },
    "nytimes": {
        "display_name": "The New York Times",
        "domain": "nytimes.com",
        "rss": [
            "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
            "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
            "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml",
            "https://rss.nytimes.com/services/xml/rss/nyt/Science.xml",
            "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
        ],
        "sitemap": "https://www.nytimes.com/sitemaps/sitemap.xml",
    },
    "wsj": {
        "display_name": "The Wall Street Journal",
        "domain": "wsj.com",
        "rss": [
            "https://feeds.a.dj.com/rss/RSSWorldNews.xml",
            "https://feeds.a.dj.com/rss/RSSUSBusiness.xml",
            "https://feeds.a.dj.com/rss/RSSWSJD.xml",
            "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
        ],
        "sitemap": "https://www.wsj.com/sitemap.xml",
    },
}
START_DATE_ISO = "2025-01-01"

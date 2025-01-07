import requests
from dateutil import parser
from django.conf import settings
from django.core.cache import cache


class BlogAPI:
    def __init__(self):
        self.url = settings.RSS_TO_JSON_URL
        self.blog_url = settings.BLOG_BASE_URL
        self.api_key = settings.RSS_TO_JSON_API_KEY
        self.payload = {
            "rss_url": settings.BLOG_BASE_URL,
            "api_key": settings.RSS_TO_JSON_API_KEY,
        }

    def get_posts(self):
        cache_key = "blog_posts"
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        try:
            response = requests.get(
                self.url,
                params=self.payload,
                timeout=settings.RSS_FEED_PULL_TIMEOUT,
            )
            if response.status_code != 200 or not response.ok:
                return f"An Error: {response.text} occurred while fetching blog posts"

            data = response.json().get("items", [])
            if not data:
                return "An Error occurred while fetching blog posts: No items found"

            # Convert the DateTime string to a Python DateTime object
            for post in data:
                post["pubDate"] = parser.parse(post["pubDate"])

            cache.set(cache_key, data, timeout=1 * 60 * 60)  # Cache for 1 hour

            return data

        except Exception as e:
            return f"An Exception: [ {e} ] occurred while fetching blog posts"

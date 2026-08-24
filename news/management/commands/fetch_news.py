import feedparser
from django.core.management.base import BaseCommand
from news.models import Article, Category

# A few beginner-friendly RSS feeds to start with
RSS_FEEDS = {
    "BBC News": "http://feeds.bbci.co.uk/news/rss.xml",
    "TechCrunch": "https://techcrunch.com/feed/",
    "BBC Business": "http://feeds.bbci.co.uk/news/business/rss.xml",
    "ESPN": "https://www.espn.com/espn/rss/news",
}


class Command(BaseCommand):
    help = "Fetches latest articles from RSS feeds and saves new ones to the database"

    def handle(self, *args, **options):
        total_new = 0

        for source_name, feed_url in RSS_FEEDS.items():
            self.stdout.write(f"Fetching from {source_name}...")
            feed = feedparser.parse(feed_url)

            for entry in feed.entries:
                # Skip if we already have this article (URL is unique)
                if Article.objects.filter(url=entry.link).exists():
                    continue

                summary = getattr(entry, "summary", "")
                published = getattr(entry, "published", None)

                Article.objects.create(
                    title=entry.title,
                    summary=summary,
                    content=summary,  # placeholder until we do full-text extraction later
                    url=entry.link,
                    source=source_name,
                    published_at=None,  # we'll parse real dates in a later step
                )
                total_new += 1

        self.stdout.write(self.style.SUCCESS(f"Done. Added {total_new} new articles."))
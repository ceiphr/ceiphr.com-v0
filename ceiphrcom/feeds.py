from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.urls import reverse
from database.models import Article

class RssSiteNewsFeed(Feed):
    title = "Ceiphr.com - All Articles"
    author_name = "Ari Birnbaum"
    feed_url = "/blog"
    link = "/blog"
    description = "Updates on changes and additions to Ceiphr.com."

    def items(self):
        return Article.objects.exclude(published=False).order_by('-modified')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.preview

    def item_link(self, item):
        return item.get_absolute_url() 

class AtomSiteNewsFeed(RssSiteNewsFeed):
    feed_type = Atom1Feed
    subtitle = RssSiteNewsFeed.description
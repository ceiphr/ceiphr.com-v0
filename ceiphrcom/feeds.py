from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.urls import reverse
from database.models import Article
import datetime

class RssSiteNewsFeed(Feed):
    title = "Ceiphr.com - All Articles"
    author_name = "Ari Birnbaum"
    author_email = 'contact@ceiphr.com'
    feed_url = "/blog"
    link = "/blog"
    description = "Updates on changes and additions to Ceiphr.com."
    feed_copyright = 'Copyright (c) 2016 - %s, Ari Birnbaum (Ceiphr). All Rights Reserved.' % datetime.date.today().year

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
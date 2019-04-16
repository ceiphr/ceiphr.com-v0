from database.models import Article
from django.urls import reverse
from django.contrib.sitemaps import Sitemap

# Static pages
class StaticViewSitemap(Sitemap):
    changefreq = 'daily'
    priority = 1.0

    def items(self):
        return ['FrontPage', 'Projects', 'Blog', 'Events', 'Skills', 'Contact']

    def location(self, item):
        return reverse(item)

# Blog pages
class BlogSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Article.objects.exclude(published=False)

    def lastmod(self, obj):
        return obj.modified

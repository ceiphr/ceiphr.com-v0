from database.models import Detail, Document, SocialLink, Project, Article, Event, Skill, Metadata
from django.urls import reverse
from django.contrib.sitemaps import Sitemap

# Static page site map
class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        return ['FrontPage', 'Projects', 'Blog', 'Events', 'Skills', 'Contact']

    def location(self, item):
        return reverse(item)

# Blog article site map
class BlogSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.modified

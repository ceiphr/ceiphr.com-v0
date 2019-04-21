from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from ceiphrcom.views import *
from django_otp.admin import OTPAdminSite
from .sitemaps import BlogSitemap, StaticViewSitemap
from .feeds import RssSiteNewsFeed, AtomSiteNewsFeed
import ceiphrcom.production_config

# Admin site details
admin.site.site_header = 'Ceiphr Control Panel'
admin.site.site_title = 'Ceiphr'

# Django 404 and 500 error catcher
handler404 = 'ceiphrcom.views.handler404'
handler500 = 'ceiphrcom.views.handler500'

sitemaps = {
    'static': StaticViewSitemap,
    'blog': BlogSitemap
}

urlpatterns = [
    # Home page - defaults to projects feed
    path('', FrontPage.as_view(template_name="index.html"), name="FrontPage"),

    # Projects page - renders project feed contents
    path('projects', Projects.as_view(
        template_name="index.html"), name="Projects"),

    # Blog page filtered by tag - renders blog post feed contents
    path('blog?t=<tag>', Blog.as_view(template_name="index.html"), name="Blog"),

    # Blog page - renders blog post feed contents
    path('blog', Blog.as_view(template_name="index.html"), name="Blog"),

    # Article page - renders selected blog post
    path('blog/<slug>', BlogPost.as_view(template_name="article.html")),

    # Blog RSS/Atom feed
    path('blog/rss20.xml', RssSiteNewsFeed()),
    path('blog/atom.xml', AtomSiteNewsFeed()),

    # Events page - renders event feed contents
    path('events', Events.as_view(template_name="index.html"), name="Events"),

    # Skills page - renders skill feed contents
    path('skills', Skills.as_view(template_name="index.html"), name="Skills"),

    # Contact page - renders contact page form
    path('contact', Contact.as_view(), name="Contact"),

    # Contact page error catcher - renders contact page contents w/ error response
    path('contact?e=<error>', Contact.as_view()),

    # Thanks (email success) page - renders thank you message on full screen template
    path('thanks', EmailSent.as_view()),

    # Site map for SEO
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap')
]

# If admin setting is enabled, the admin URL is available to manage Django's DB
if settings.ADMIN_ENABLED:
    urlpatterns += [
        path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
        path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
        path(ceiphrcom.production_config.adminURLHash+'/admin', admin.site.urls),
    ]

# For test server during development - allows for media to be retrieved
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
else:
    # TOTP for production
    admin.site.__class__ = OTPAdminSite

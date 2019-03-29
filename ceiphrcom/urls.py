from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from ceiphrcom.views import *
from django_otp.admin import OTPAdminSite
import ceiphrcom.production_config

# Admin site details
admin.site.site_header = 'Ceiphr Control Panel'
admin.site.site_title = 'Ceiphr'

# Django 404 and 500 error catcher
handler404 = 'ceiphrcom.views.handler404'
handler500 = 'ceiphrcom.views.handler500'

urlpatterns = [
    # Home page - defaults to projects feed
    path('', FrontPage.as_view(template_name="index.html")),

    # Projects page - renders project feed contents
    path('projects', Projects.as_view(template_name="index.html")),

    # Blog page - renders blog post feed contents
    path('blog', Blog.as_view(template_name="index.html")),

    # Article page - renders selected blog post
    path('blog/<slug>', BlogPost.as_view(template_name="article.html")),

    # Events page - renders event feed contents
    path('events', Events.as_view(template_name="index.html")),

    # Skills page - renders skill feed contents
    path('skills', Skills.as_view(template_name="index.html")),

    # Contact page - renders contact page form
    path('contact', Contact.as_view()),

    # Contact page error catcher - renders contact page contents w/ error response
    path('contact?e=<error>', Contact.as_view()),

    # Thanks (email success) page - renders thank you message on full screen template
    path('thanks', EmailSent.as_view())
]

# If admin setting is enabled, the admin URL is available to manage Django's DB
if settings.ADMIN_ENABLED:
    urlpatterns += [
        path(ceiphrcom.production_config.adminURLHash+'/admin', admin.site.urls),
    ]

# For test server during development - allows for media to be retrieved
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # TOTP for production
    admin.site.__class__ = OTPAdminSite


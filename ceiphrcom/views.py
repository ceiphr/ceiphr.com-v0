from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic import TemplateView
from database.models import Detail, Document, SocialLink, Project, Article, Event, Skill, Metadata
from django.core.mail import BadHeaderError, EmailMessage
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from .forms import ContactForm
import random
import datetime

# Generic metadata for pages rendered with index.html template


class IndexMetadata(object):
    def get_context_data(context, slug=""):
        # Page metadata
        try:
            exists = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            exists = None

        if slug and exists:
            context["article_metadata"] = Article.objects.values("title", "preview", "image").get(slug=slug)
            context["is_article"] = True
        else:
            context["is_article"] = False
        
        if Metadata.objects.all():
            context["metadata"] = random.choice(Metadata.objects.all())

        if Detail.objects.all():
            # Portfolio owner details
            context["username"] = Detail.objects.first().user_name
            context["name"] = Detail.objects.first().legal_name
            context["logo"] = Detail.objects.first().logo
            context["phone"] = Detail.objects.first().phone
            context["email"] = Detail.objects.first().email
            context["document"] = Document.objects.first().document
            context["links"] = SocialLink.objects.all()

        context["thisYear"] = datetime.date.today().year
        # Sass rain droplet elements
        dropletCount = 30
        context["rain_range"] = range(dropletCount)
        return context


# Email response system


class EmailSent(View):
    def get(self, request, view="projects"):
        context = dict()
        context["view"] = "Thanks"
        context = IndexMetadata.get_context_data(context)
        return render(request, 'thanks.html', context)


# Error catching with full page - 404


def handler404(request, exception, template_name='404.html'):
    context = dict()
    context["view"] = "404"
    context = IndexMetadata.get_context_data(context)
    return render(request, '404.html', context, status=404)

# Error catching with full page - 500


def handler500(request, exception, template_name='500.html'):
    context = dict()
    context["view"] = "404"
    context = IndexMetadata.get_context_data(context)
    return render(request, '500.html', context, status=500)

# FromtPage feed for index template


class FrontPage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context = IndexMetadata.get_context_data(context)
        context["projects"] = Project.objects.all()
        context["articles"] = Article.objects.all()
        context["events"] = Event.objects.all()
        context["view"] = "FrontPage"
        return context

# Article template
class BlogPost(TemplateView):
    template_name = 'article.html'

    def get_context_data(self, slug, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context = IndexMetadata.get_context_data(context, slug)
        context["articles"] = Article.objects.exclude(slug=slug)
        try:
            exists = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            exists = None
        if exists:
            context["contents"] = Article.objects.get(slug=slug)
        else: 
            raise Http404
        context["view"] = "Blog"
        return context
        
# Blog feed for index template


class Blog(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context = IndexMetadata.get_context_data(context)
        context["contents"] = Article.objects.all()
        context["view"] = "Blog"
        return context

# Project feed for index template


class Projects(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context = IndexMetadata.get_context_data(context)
        context["contents"] = Project.objects.all()
        context["view"] = "Projects"
        return context

# Project feed for index template


class Events(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context = IndexMetadata.get_context_data(context)
        context["contents"] = Event.objects.all()
        context["view"] = "Events"
        return context

# Skills feed for index template


class Skills(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context = IndexMetadata.get_context_data(context)
        context["contents"] = Skill.objects.all()
        context["view"] = "Skills"
        return context

# Contact page for index template


class Contact(View):
    # Contact form handler
    def contact_form(self, request):
        context = dict()
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = ContactForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                sender = [form.cleaned_data['sender']]

                sender_subject = "%s | Ceiphr" % form.cleaned_data['subject']
                sender_copy = 'Thank you for the email. Here is a copy of what you sent me: \n\n"'\
                            +form.cleaned_data['message']\
                            +'"\n\nThis is an automated response. I will get back to you shortly.\n\nBest Regards,\nAri'

                receiver = ["contact@ceiphr.com"]

                receiver_subject = form.cleaned_data['subject']
                receiver_copy = form.cleaned_data['message']
  
                mail_server = "Ari Birnbaum (Ceiphr) <noreply@mail.ceiphr.com>"

                # Make copy of message for the sender
                sender_email = EmailMessage(sender_subject, sender_copy, mail_server, sender, reply_to=receiver)
                
                # Make copy of message for my email address
                receiver_email = EmailMessage(receiver_subject, receiver_copy, mail_server, receiver, reply_to=sender)
                try:
                    sender_email.send(fail_silently=False)
                    receiver_email.send(fail_silently=False)
                    return True
                except BadHeaderError:
                    return False
            else:
                return False
        # if a GET (or any other method) we'll create a blank form
        else:
            form = ContactForm()
        return form

    def get(self, request):
        context = dict()
        context = IndexMetadata.get_context_data(context)
        context["view"] = "Contact"
        context["contents"] = self.contact_form(request)
        # Error catcher
        error = request.GET.get('e', '')
        if error == "incomplete-form":
            context["incomplete_form"] = True
        return render(request, 'index.html', context)

    def post(self, request, view=None):
        success = self.contact_form(request)
        if success:
            return HttpResponseRedirect("/thanks")
        else:
            return HttpResponseRedirect("/contact?e=incomplete-form")

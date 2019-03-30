from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
from django import forms
import ceiphrcom.production_config

class ContactForm(forms.Form):
    # Sender field - validated via MaterializeCSS framework (validate class) and via Django's EmailField
    sender = forms.EmailField(widget=forms.TextInput(attrs={'required': True, 'id':"sender", 'placeholder':"elonmusk@tesla.com", 'type':"email", 'class':"validate"}))
    
    # Subject field - body of email
    subject = forms.CharField(widget=forms.TextInput(attrs={'required': True, 'id':"subject", 'placeholder':"Wow Ari, you sure are the best!", 'type':"text", 'class':"validate"}))
    
    # Message field - body of email
    message = forms.CharField(widget=forms.Textarea(attrs={'required': True, 'id':"message", 'placeholder':"My master's thesis on turtles...", 'type':"text", 'class':"materialize-textarea validate"}))
    
    if not ceiphrcom.production_config.debug:
        # Captcha field - are you a robot? We'll find out.
        captcha = ReCaptchaField(widget=ReCaptchaWidget(attrs={'required': True}))

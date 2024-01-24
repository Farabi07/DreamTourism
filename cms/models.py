from distutils.command.upload import upload
import imp
from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
# Create your models here.

class CMSMenu(models.Model):
    parent = models.ForeignKey('self', on_delete=models.PROTECT, related_name='children', null=True, blank=True)
    name = models.CharField(max_length=255)
    position = models.IntegerField(unique=True, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)

    class Meta:
        verbose_name_plural = 'CMSMenus'
        ordering = ('-id', )

    def __str__(self):
        return self.name
	
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



class CMSMenuContent(models.Model):
    cms_menu = models.ForeignKey(CMSMenu, on_delete=models.PROTECT, related_name='cms_menu_contents')
    name = models.TextField()
    value = models.TextField()
    description = models.TextField(null=True, blank=True)
    duration = models.CharField(max_length=100,null=True, blank=True)
    inclution = models.TextField(null=True, blank=True)
    exclusion = models.TextField(null=True, blank=True)
    url = models.CharField(max_length=1000, null=True, blank=True)
    price = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)

    class Meta:
        verbose_name_plural = 'CMSMenuContents'
        ordering = ('-id', )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



class CMSMenuContentImage(models.Model):
    cms_menu = models.ForeignKey(CMSMenu, on_delete=models.PROTECT, related_name='cms_menu_content_images')
    head = models.CharField(max_length=500)
    image = models.ImageField(upload_to='cms/ContentImage/')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)

    class Meta:
        verbose_name_plural = 'CMSMenuContentImages'
        ordering = ('-id', )

    def __str__(self):
        return self.head

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



 
#add this
class Itinerary(models.Model):
    cms_content = models.ForeignKey(CMSMenuContent, on_delete=models.PROTECT,null=True,blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=1000, null=True, blank=True)
     
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Itinerary'
        ordering = ('-id', )

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)       


#For Contact



class EmailAddress(models.Model):
    full_name = models.CharField(max_length=255,null=True, blank=True)
    email = models.EmailField(null=False, blank=False)
    subject = models.CharField(max_length=255,null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = 'Contact'
        ordering = ('-id', )

    def __str__(self):
        return self.email
    
@receiver(post_save, sender=EmailAddress)
def send_email_on_new_signup(sender, instance, created, **kwargs):
    if created:
        # Send contact confirmation email
        subject = 'New Customer Contact With us'
        message = f'Customer Details,\n\n'
        message += f'Full Name: {instance.full_name}\n'
        message += f'Email: {instance.email}\n'
        message += f'Subject: {instance.subject}\n'
        message += f'Message: {instance.message}\n'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = ['sales@dreamziarah.com',]
        send_mail(subject, message, from_email, recipient_list)

        # Send feedback email to the sender
        feedback_subject = 'Your Journey Awaits with Dream Tourism'
        feedback_message = render_to_string('contactUs_feedback.html')
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [instance.email]
        send_mail(
            feedback_subject,
            '',
            from_email,
            recipient_list,
            html_message=feedback_message,
        )

#For Subscription

class SendEmail(models.Model):
   
    email = models.EmailField(null=False, blank=False)
    class Meta:
        verbose_name_plural = 'Send Email'
        ordering = ('-id', )

    def __str__(self):
        return self.email
    
@receiver(post_save, sender=SendEmail)
def send_email(sender, instance, created, **kwargs):
    if created:
        subject = 'New Email Subscription'
        message = render_to_string('subscription_confirmation_email.html', {'email': instance.email})

        from_email = settings.EMAIL_HOST_USER
        recipient_list = ['sales@dreamziarah.com', 'farhadkabir1212@gmail.com']
        send_mail(
            subject,
            '',
            from_email,
            recipient_list,
            html_message=message,
        )
        feedback_subject = "Welcome to Dream Tourism's Travel Community!"
        feedback_message = render_to_string('welcome_email.html')

        from_email = settings.EMAIL_HOST_USER
        recipient_list = [instance.email]
        send_mail(
            feedback_subject,
            '',
            from_email,
            recipient_list,
            html_message=feedback_message,
        )
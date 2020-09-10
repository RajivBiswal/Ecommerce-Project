from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.db.models.signals import pre_save, post_save

from accounts.signals import user_logged_in
from analytics.signals import object_viewed_signal
from analytics.utils import get_client_ip

User = settings.AUTH_USER_MODEL

FORCE_SESSION_TO_ONE = getattr(settings, 'FORCE_SESSION_TO_ONE', False)
FORCE_INACTIVE_USER_ENDSESSION = getattr(settings, 'FORCE_INACTIVE_USER_ENDSESSION', False)

class ObjectViewed(models.Model):
    user                = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    ip_address          = models.CharField(max_length=255, blank=True, null=True)
    content_type        = models.ForeignKey(ContentType, on_delete=models.CASCADE) # Any of our models like products,order,address
    object_id           = models.PositiveIntegerField() # Id of the model - products.id,User.id, order.id
    content_object      = GenericForeignKey('content_type', 'object_id') #product instance
    timestamp           = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s viewed %s" %(self.content_object, self.timestamp)

    class Meta:
        ordering            = ['-timestamp']    #most recent shows first
        verbose_name        = 'Object viewed'
        verbose_name_plural = 'Objects viewed'

def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender) #same like instance.__class__

    new_viewed_obj = ObjectViewed.objects.create(
                    user=request.user,
                    content_type = c_type,
                    object_id = instance.id,
                    ip_address = get_client_ip(request)
    )

object_viewed_signal.connect(object_viewed_receiver)


class UserSession(models.Model):
    user                = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    ip_address          = models.CharField(max_length=255, blank=True, null=True)
    session_key         = models.CharField(max_length=100, blank=True, null=True)
    timestamp           = models.DateTimeField(auto_now_add=True)
    active              = models.BooleanField(default=True)
    ended               = models.BooleanField(default=False)

    def end_session(self):
        session_key = self.session_key
        ended = self.ended
        try:
            Session.objects.get(pk=session_key).delete()
            self.ended = True
            self.active = False
            self.save()
        except:
            pass
        return self.ended

def post_save_session_reciever(sender, created, instance, *args, **kwargs):
    """ending session to prevent multiple login for same user"""
    if created:
        qs = UserSession.objects.filter(user=instance.user, ended=False, active=False).exclude(id=instance.id)
        for i in qs:
            i.end_session()
    if not instance.ended and not instance.active:
        instance.end_session()

if FORCE_SESSION_TO_ONE:
    post_save.connect(post_save_session_reciever,sender=UserSession)

def post_save_user_changed_receiver(sender, created, instance, *args, **kwargs):
    """end session if the user is no longer active"""
    if not created:
        if instance.is_active==False:
            qs = UserSession.objects.filter(user=instance.user, ended=False,active=False)
            for i in qs:
                i.end_session()

if FORCE_INACTIVE_USER_ENDSESSION:
    post_save.connect(post_save_user_changed_receiver, sender=User)

def user_logged_in_receiver(sender, instance, request, *args, **kwargs):
    """create a session for login user & get session GenericForeignKey"""
    print(instance)
    user = instance
    ip_address = get_client_ip(request)
    session_key = request.session.session_key
    UserSession.objects.create(
            user=user,
            ip_address=ip_address,
            session_key=session_key
    )


user_logged_in.connect(user_logged_in_receiver)

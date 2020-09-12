from django.db import models
from django.conf import settings
from django.db.models.signals import post_save,pre_save


from accounts.models import GuestModel
User = settings.AUTH_USER_MODEL


import stripe
stripe.api_key = "sk_test_51HQ4O7ChXO4h6peOR6oFLbvv5GTIyBjwMAKiTvw2qIHEeTlAPsjJctx0sn85BXb9wFUAM89IABbpSR018mZRU5f000oPGKCiHU"

class BillingProfileManager(models.Manager):
    """creating a manger that handle billing_profile for logged in user or guest"""
    def new_or_get(self,request):
        user = request.user
        guest_model_id = request.session.get('guest_model_id')
        created = False
        obj = None

        if user.is_authenticated:
            """logged-in user checkout.remember payment stuff"""
            obj, created = self.model.objects.get_or_create(
                                                            user=user,email=user.email)
        elif guest_model_id is not None:
            """guest user checkout.auto reload payment stuff"""
            guest_model_obj = GuestModel.objects.get(id=guest_model_id)
            obj, created = self.model.objects.get_or_create(
                                                            email=guest_model_obj.email)
        else:
            pass
        return obj, created


#an email might have 1000 billing profile
#but user of same email has only 1 billing profile
class BillingProfile(models.Model):
    user        = models.OneToOneField(User, null=True, blank=True,
                                        on_delete=models.CASCADE)
    email       = models.EmailField()
    active      = models.BooleanField(default=True)
    update      = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    customer_id  = models.CharField(max_length=255, null=True,blank=True)    #for Braintree/Srtipe

    objects = BillingProfileManager()

    def __str__(self):
        return self.email

def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance,email=instance.email)

post_save.connect(user_created_receiver, sender=User)

"""For Stripe or Braintree"""
def billing_profile_created_receiver(sender, instance, *args, **kwargs):
    if not instance.customer_id and instance.email:
        print('API Request sent to Stripe/Braintree')
        customer = stripe.Customer.create(
            email = instance.email
        )
        instance.customer_id = customer.id

pre_save.connect(billing_profile_created_receiver, sender=BillingProfile)

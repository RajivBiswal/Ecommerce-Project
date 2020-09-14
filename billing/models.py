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

    def charge(self, order_obj, card=None):
        return Charge.objects.create_charge(self, order_obj, card)

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


class CardManager(models.Manager):
    def add_new(self, billing_profile, card_response):
        if str(card_response.object) == 'card':
            new_card = self.model(
                billing_profile = billing_profile,
                stripe_id       = card_response.id,
                brand           = card_response.brand,
                country         = card_response.country,
                exp_month       = card_response.exp_month,
                exp_year        = card_response.exp_year,
                last4           = card_response.last4
            )
            new_card.save()
            return new_card

        return None


class Card(models.Model):
    """create a card with strie id"""
    billing_profile      = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    stripe_id            = models.CharField(max_length=255, null=True,blank=True)
    brand                = models.CharField(max_length=120, null=True,blank=True)
    country              = models.CharField(max_length=20, null=True,blank=True)
    exp_month            = models.IntegerField(null=True,blank=True)
    exp_year             = models.IntegerField(null=True,blank=True)
    last4                = models.CharField(max_length=4,null=True,blank=True)
    default              = models.BooleanField(default=True)

    objects = CardManager()

    def __str__(self):
        return "{} {}".format(self.brand, self.last4)



class ChargeManager(models.Manager):
    def create_charge(self,billing_profile, order_obj, card=None):
        card_obj = card
        if card_obj is None:
            cards = billing_profile.card_set.filter(default=True)
            if cards.exists():
                card_obj = cards.first()
        if card_obj is None:
            return False, "No cards are available"

        c = stripe.Charge.create(
              amount= int(order_obj.total * 100),
              currency="inr",
              source= card_obj.stripe_id ,
              customer = billing_profile.customer_id,
              metadata={'order_id': order_obj.order_id}
            )

        new_charge = self.model(
            billing_profile     = billing_profile,
            stripe_id           = c.stripe_id,
            paid                = c.paid,
            refunded            = c.refunded,
            outcome             = c.outcome,
            outcome_type        =c.outcome['type'],
            seller_message      =c.outcome.get('seller_message'),
            risk_level          =c.outcome.get('risk_level')

        )
        new_charge.save()
        return new_charge.paid,new_charge.seller_message

class Charge(models.Model):
    billing_profile     = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    stripe_id           = models.CharField(max_length=255, null=True,blank=True)
    paid                = models.BooleanField(default=False)
    refunded            = models.BooleanField(default=False)
    outcome             = models.TextField(null=True, blank=True)
    outcome_type        = models.CharField(max_length=120,null=True, blank=True)
    seller_message      = models.CharField(max_length=120,null=True, blank=True)
    risk_level          = models.CharField(max_length=120,null=True, blank=True)

    objects = ChargeManager()

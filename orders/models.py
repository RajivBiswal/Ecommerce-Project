import math

from django.db import models
from django.db.models.signals import pre_save,post_save

from carts.models import Cart
from billing.models import BillingProfile
from ecommerce_project.utils import unique_order_id_generator
from address.models import Address

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('delivered','Delivered'),
    ('refunded', 'Refunded'),
)


class OrderManager(models.Manager):
    """checking billing_profile exists or not if not then create one & pass it
        to carts views"""
    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset().filter(
                        billing_profile=billing_profile,
                        cart=cart_obj,
                        active=True,
                        status= 'created')
        if qs.count()==1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(
                    billing_profile=billing_profile,
                    cart=cart_obj)
            created = True
        return obj, created


class Order(models.Model):
    """Creating order components"""
    order_id        = models.CharField(max_length=120,blank=True)
    billing_profile = models.ForeignKey(BillingProfile,
                                null=True,blank=True,
                                on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(Address,
                                related_name='shipping_address',
                                null=True,blank=True,
                                on_delete=models.CASCADE)
    billing_address = models.ForeignKey(Address,
                                related_name='billing_address',
                                null=True,blank=True,
                                on_delete=models.CASCADE)
    cart            = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status          = models.CharField(max_length=10,default='created',
                                        choices=ORDER_STATUS_CHOICES)
    active          = models.BooleanField(default=True)
    shipping_total  = models.DecimalField(default=20.00,
                                            max_digits=10,
                                            decimal_places=2)
    total           = models.DecimalField(default=0.00,
                                            max_digits=10,
                                            decimal_places=2)

    objects = OrderManager()
    def __str__(self):
        return self.order_id

    def update_total(self):
        """"updating the cart total after adding shipping total"""
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = math.fsum([cart_total , shipping_total])
        self.total = new_total
        self.save()
        return new_total

    def check_done(self):
        """check out whether all these parameters exists"""
        billing_profile = self.billing_profile
        shipping_address = self.shipping_address
        billing_address = self.billing_address
        total = self.total
        if billing_profile and shipping_address and billing_address and total > 0:
            return True
        return False

    def check_paid(self):
        """checking out whether its paid or not"""
        if self.check_done():
            self.status = 'paid'
            self.save()
        return self.status

def pre_save_create_order_id(sender, instance, *args, **kwargs):
    """
    This will assign a unique id to order id before Order model updates in db
    """
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
        qs = Order.objects.filter(cart=instance.cart).exclude(
                            billing_profile=instance.billing_profile)
        if qs.exists():     #if instance of cart other than billing_profile exists in orders then update the active field
            qs.update(active=False)

pre_save.connect(pre_save_create_order_id, sender=Order)

def post_save_cart_total(sender, instance, created, *args, **kwargs):
    """
    This will count filter the cart item and count the cart total
    """
    cart_total = instance.total
    qs = Order.objects.filter(cart__id = instance.id) #more like cart__iexact
    if qs.count()== 1:
        order_obj = qs.first()
        order_obj.update_total()

post_save.connect(post_save_cart_total, sender=Cart)

def post_save_order(sender,instance, created, *args, **kwargs):
    """
    This will count total values of orders
    """
    if created:
        instance.update_total()

post_save.connect(post_save_order,sender=Order)

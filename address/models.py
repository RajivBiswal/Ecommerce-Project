from django.db import models

from billing.models import BillingProfile

ADDRESS_TYPE = (
    ('billing','Billing'),
    ('shipping','Shipping'),
)

class Address(models.Model):
    billing_profile     = models.ForeignKey(BillingProfile,on_delete=models.CASCADE)
    address_type        = models.CharField(max_length=100, choices=ADDRESS_TYPE)
    address_line1       = models.CharField(max_length=100)
    address_line2       = models.CharField(max_length=100,blank=True,null=True)
    city                = models.CharField(max_length=100)
    state               = models.CharField(max_length=100)
    country             = models.CharField(max_length=100, default='India')
    pin_code            = models.CharField(max_length=100)

    def __str__(self):
        return str(self.billing_profile)

    def get_address(self):
        return "{line1}\n{line2}\n{city}\n{state}, {pin}\n{country}".format(
                line1 = self.address_line1,
                line2 = self.address_line2 or "",
                city = self.city,
                state = self.state,
                pin = self.pin_code,
                country = self.country
        )

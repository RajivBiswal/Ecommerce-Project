from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse

from products.models import MyProduct
from ecommerce_project.utils import unique_slug_generator

class Tag(models.Model):
    """Creating tags for products"""
    title = models.CharField(max_length=120)
    slug = models.SlugField()
    timestamp = models.DateTimeField(auto_now_add=True)
    products =  models.ManyToManyField(MyProduct, blank=True)

    def __str__(self):
        return self.title


def tags_pre_save_receiver(sender, instance, *args, **kwargs):
    """change the slug field value with unique generator before model are save"""
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(tags_pre_save_receiver, sender = Tag)

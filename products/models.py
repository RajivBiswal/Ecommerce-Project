import random,os
from django.db import models
from django.db.models.signals import pre_save
from django.db.models import Q

from django.urls import reverse

from ecommerce_project.utils import unique_slug_generator

def get_filename_ext(filepath):
    """split the file name and extension"""
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    """create a filename with a random interger"""
    new_filename = random.randint(1,3980506710)
    name, ext = get_filename_ext(filename)
    final_filename = f'{new_filename}{ext}'
    return "products/{new_filename}/{final_filename}".format(
                    new_filename=new_filename,
                    final_filename=final_filename
                     )

class MyProductManager(models.Manager):
    """Creating a manager class for our products"""

    def featured(self):
        return self.get_queryset().filter()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self,query):
        lookups = ( Q(title__icontains=query)|
                    Q(description__icontains=query)|
                    Q(tag__title__icontains=query)
                    )
        return self.get_queryset().filter(lookups).distinct()

class MyProduct(models.Model):
    """Creating a model for the app"""
    title       = models.CharField(max_length=255)
    slug        = models.SlugField(blank=True,unique=True)
    description = models.TextField()
    price       = models.DecimalField(decimal_places=2,
                                        max_digits=19,
                                        null=True)
    image      = models.ImageField(upload_to= upload_image_path,
                                    null = True,blank=True)
    featured   = models.BooleanField(default=False)

    objects = MyProductManager()

    def get_absolute_url(self):
        """assigning a url in product list"""
        return "/products/{slug}/".format(slug=self.slug)
        # return reverse("products:detail", kwargs={"slug":self.slug })

    def __str__(self):
        return self.title


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    """change the slug field value with unique generator before model are save"""
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender = MyProduct)

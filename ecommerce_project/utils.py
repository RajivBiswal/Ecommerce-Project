import random
import string
from django.utils.text import slugify

def random_string_generator(size=10,chars = string.ascii_lowercase + string.digits):
    """Creating unique strings values"""
    return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator(instance, new_slug=None):
    """Creating unique slugs for every products if slug exists then keep it
    as it is if not then create one with the title of the product"""
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug, randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)

    return slug

def unique_order_id_generator(instance):
    """Create a unique order_id for oreders app"""
    new_order_id = random_string_generator().upper()
    Klass = instance.__class__
    qs_value = Klass.objects.filter(order_id=new_order_id).exists()
    if qs_value:
        return unique_slug_generator(instance)
    return new_order_id

from django.shortcuts import render
from django.views import generic
from django.http import Http404

from products import models
from carts.models import Cart
from analytics.signals import ObjectViewedMixin


class ProductListView(generic.ListView):
    """Creating a list of view for the product"""
    # queryset = models.MyProduct.objects.all()
    template_name = 'products/list.html'
    slug_url_kwarg = 'the_slug'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return models.MyProduct.objects.all()


class ProductSlugDetailView(ObjectViewedMixin, generic.DetailView):
    """Using for slug field"""
    queryset = models.MyProduct.objects.all()
    template_name = 'products/detail.html'
    slug_url_kwarg = 'the_slug'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductSlugDetailView,self).get_context_data(*args,**kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context


class ProductFeaturedListView(generic.ListView):
    template_name = 'products/list.html'

    def get_queryset(self,*args, **kwargs):
        request = self.request
        return models.MyProduct.objects.featured()


class ProductFeaturedDetailView(ObjectViewedMixin, generic.DetailView):
    template_name = 'products/featured-detail.html'
    queryset = models.MyProduct.objects.featured()


class HomepageView(generic.TemplateView):
    """Homepage of the project"""
    template_name  = 'home_page.html'


class ContactView(generic.TemplateView):
    """Contact Info"""
    template_name = 'contact.html'

class AboutView(generic.TemplateView):
    """About the page"""
    template_name = 'about.html'

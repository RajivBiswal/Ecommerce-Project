from django.shortcuts import render
from django.views.generic import ListView

from products.models import MyProduct

class SearchProductView(ListView):
    template_name = 'search/view.html'

    def queryset(self, *args, **kwargs):
        request= self.request
        query = request.GET.get('q')
        if query is not None:

            return MyProduct.objects.search(query)
        return MyProduct.objects.featured()

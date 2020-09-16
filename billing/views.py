from django.conf import settings
from django.shortcuts import render,redirect
from django.http import JsonResponse, HttpResponse
from django.utils.http import is_safe_url

from billing.models import BillingProfile,Card

import stripe
STRIPE_SECRET_KEY = getattr(settings, 'STRIPE_SECRET_KEY')
STRIPE_PUB_KEY = getattr(settings, 'STRIPE_PUB_KEY')
stripe.api_key = STRIPE_SECRET_KEY

def payment_method_view(request):
    """If there is a billing profile show the stripe card page"""
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if not billing_profile:
        return redirect("/")
    next_url = None
    next_ = request.GET.get('next')
    if is_safe_url(next_, request.get_host()):
        next_url = next_

    return render(request,'billing/payment-method.html',{'publish_key':STRIPE_PUB_KEY, 'next_url': next_url})


def payment_create_view(request):
    """create or add a new card with stripe"""
    if request.method == 'POST' and request.is_ajax():
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return HttpResponse({'message': 'Can not find this user!'}, status_code=404)

        token = request.POST.get('token')

        if token is not None:
            new_card_obj = Card.objects.add_new(billing_profile, token)
            # new_card_obj = Card.objects.add_new(billing_profile, card_response)
        return JsonResponse({'message':'Success! your card is added'})
    return HttpResponse('Error occoured!!', status_code=404)

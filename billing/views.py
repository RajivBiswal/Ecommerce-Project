from django.shortcuts import render,redirect
from django.http import JsonResponse, HttpResponse
from django.utils.http import is_safe_url
from billing.models import BillingProfile,Card

import stripe
stripe.api_key = "sk_test_51HQ4O7ChXO4h6peOR6oFLbvv5GTIyBjwMAKiTvw2qIHEeTlAPsjJctx0sn85BXb9wFUAM89IABbpSR018mZRU5f000oPGKCiHU"
STRIPE_PUB_KEY = "pk_test_51HQ4O7ChXO4h6peOe0nUuYob3ROqijPykAZ8beuv7BCs5YM7saWf3EJyFC3yMhKNAy7buDqPXRgiLU3xxv4C5KAe00Ecl6YW0Q"

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
            card_response = stripe.Customer.create_source(
                              billing_profile.customer_id,
                              source=token,
                            )
            new_card_obj = Card.objects.add_new(billing_profile, card_response)
            print(new_card_obj)
        return JsonResponse({'message':'Success! your card is added'})
    return HttpResponse('Error occoured!!', status_code=404)

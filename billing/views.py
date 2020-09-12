from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.utils.http import is_safe_url

import stripe
stripe.api_key = "sk_test_51HQ4O7ChXO4h6peOR6oFLbvv5GTIyBjwMAKiTvw2qIHEeTlAPsjJctx0sn85BXb9wFUAM89IABbpSR018mZRU5f000oPGKCiHU"
STRIPE_PUB_KEY = "pk_test_51HQ4O7ChXO4h6peOe0nUuYob3ROqijPykAZ8beuv7BCs5YM7saWf3EJyFC3yMhKNAy7buDqPXRgiLU3xxv4C5KAe00Ecl6YW0Q"

def payment_method_view(request):
    next_url = None
    next_ = request.GET.get('next')
    if is_safe_url(next_, request.get_host()):
        next_url = next_

    return render(request,'billing/payment-method.html',{'publish_key':STRIPE_PUB_KEY, 'next_url': next_url})


def payment_create_view(request):
    if request.method == 'POST' and request.is_ajax():
        print(request.POST)
        return JsonResponse({'message':'Success! your card is added'})
    return HttpResponse('Error occoured!!', status_code=404)

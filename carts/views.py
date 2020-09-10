from django.http import JsonResponse
from django.shortcuts import render, redirect

from carts.models import Cart
from products.models import MyProduct
from orders.models import Order
from accounts.forms import LoginForm,GuestForm
from accounts.models import GuestModel
from billing.models import BillingProfile
from address.forms import AddressForm
from address.models import Address

def cart_deail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [{
                "title":x.title,
                "price": x.price,
                "id": x.id,
                "url": x.get_absolute_url(),
                }
                 for x in cart_obj.products.all() ]
    cart_data = {
            "products": products,
            "subtotal": cart_obj.subtotal,
            "total": cart_obj.total,
        }
    return JsonResponse(cart_data)


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, 'carts/home.html', {'cart':cart_obj})

def cart_update(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = MyProduct.objects.get(id=product_id)
        except MyProduct.DoesNotExist:
            return redirect('carts:home')
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            added = False
        else:
            cart_obj.products.add(product_obj)
            added = True
        request.session['total_items'] = cart_obj.products.count()

        if request.is_ajax():
            json_data = {
                "added": added,
                "removed": not added,
                "totalItemsCount":cart_obj.products.count(),
            }
            return JsonResponse(json_data, status=200)
    return redirect('carts:home')

def checkout_home(request):
    """Implementing checkout process"""
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect('carts:home')

    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get('shipping_address_id', None)


    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None

    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile,
                                                                    cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(
                                            id=shipping_address_id)
            del request.session['shipping_address_id']
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(
                                            id = billing_address_id)
            del request.session['billing_address_id']
        if shipping_address_id or billing_address_id:
            order_obj.save()

    if request.method == 'POST':
        """check if there is a order and its paid then delete the session cart__id
            and redirect to some success page"""
        is_done = order_obj.check_done()
        if is_done:
            order_obj.check_paid()
            del request.session['cart_id']
            request.session['total_items'] = 0
            return redirect('carts:success')

    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        'guest_form': guest_form,
        'address_form': address_form,
        'address_qs': address_qs,
    }
    return render(request, "carts/checkout.html",context)


def checkout_done(request):
    return render(request, "carts/checkout-done.html",{})
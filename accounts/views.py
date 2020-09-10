from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model,login,authenticate
from django.utils.http import is_safe_url
from django.urls import reverse_lazy

from django.views.generic import FormView,CreateView

from accounts.forms import LoginForm,RegisterForm,GuestForm
from accounts.models import GuestModel
from accounts.signals import user_logged_in


def guest_register_view(request):
    """for guest user"""
    form = GuestForm(request.POST or None)
    context = {'form':form}
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        email = form.cleaned_data.get('email')
        new_guest_model = GuestModel.objects.create(email=email)
        request.session['guest_model_id'] = new_guest_model.id
        if is_safe_url(redirect_path,request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect('accounts:register')
    return redirect('accounts:register')


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'accounts/login_page.html'
    success_url = '/'

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None

        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            user_logged_in.send(user.__class__, instance=user, request=request) #sending the signal
            try:
                del request.session['guest_model_id']
            except:
                pass
            if is_safe_url(redirect_path,request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")

        return super(LoginView, self).form_invalid(form)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register_page.html'
    success_url = reverse_lazy('accounts:login')



"""function based login view"""
# def login_page(request):
#     form = LoginForm(request.POST or None)
#     context = {'form':form}
#     next_ = request.GET.get('next')
#     next_post = request.POST.get('next')
#     redirect_path = next_ or next_post or None
#
#     if form.is_valid():
#         username = form.cleaned_data.get("username")
#         password = form.cleaned_data.get("password")
#         user = authenticate(request, username=username, password=password)
#
#         if user is not None:
#             login(request, user)
#             try:
#                 del request.session['guest_model_id']
#             except:
#                 pass
#             if is_safe_url(redirect_path,request.get_host()):
#                 return redirect(redirect_path)
#             else:
#                 return redirect("/")
#         else:
#             print("Error")
#     return render(request, "accounts/login_page.html", context)


"""function based register view"""
# User = get_user_model()
# def register_page(request):
#     form = RegisterForm(request.POST or None)

    # if form.is_valid():
    #     form.save()
    #
    #     """used for normal form"""
    #     # username = form.cleaned_data.get("username")
    #     # email = form.cleaned_data.get("email")
    #     # password = form.cleaned_data.get("password")
    #     # new_user = User.objects.create_user(username, email, password)
    #     #
    #     # if new_user:
    #     #     return redirect("/")
    #     """"""
    # return render(request, "accounts/register_page.html", {"form": form})

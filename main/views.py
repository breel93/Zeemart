from django.shortcuts import render
from django.utils.http import is_safe_url
from django.views.generic import TemplateView, CreateView, FormView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, authenticate, login
from .forms import RegistrationForm, UpdateCustomerForm,UpdateCustomerFormTwo,LoginForm
from .signals import user_logged_in
from products.models import Category, SubCategory,SubSubCategory, Product
from random import shuffle
# Create your views here.
# def home_page(request):
#     return render(request, "home_page.html", {})

class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self,*args, **kwargs):
        category      = Category.objects.all()[:7]
        subcategory   = SubCategory.objects.all()
        subsubcategory  = SubSubCategory.objects.all()
        featured_product = list(Product.objects.filter(featured = True))[:12]
        shuffle(featured_product)
        context = { 'category':category,
                'subcategory': subcategory,
                'subsubcategory': subsubcategory,
                'featured_product': featured_product }
        return context

# def subcategory_list(request, slug):
#     subcategory   = SubCategory.objects.filter(category__slug=slug)
#     print(subcategory)
#     # category      = Category.objects.all()[:7]
#     context = {'subcategory': subcategory}
#     return render(request,'main/index.html', context)


def subcategory_list(request, slug):
    subcategory   = SubCategory.objects.filter(category__slug=slug)
    print(subcategory)
    # category      = Category.objects.all()[:7]
    context = {'subcategory': subcategory}
    return render(request,'main/index.html', context)

    



def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST) #from our registration form class in form.py, we get the request method

        if form.is_valid():
            form.save()

            email = request.POST.get('email')
            password = request.POST.get('password1')


            user = authenticate(
                request,
                email = email,
                password = password
            )
            login(request, user)
            return redirect(reverse('main:index'))
    else:
        form = RegistrationForm()
    args = {'form':form} 
    return render(request, 'main/reg_form.html',args) 


def customer_profile(request):
    if request.method == "POST":
        form = UpdateCustomerForm(request.POST, instance=request.user,prefix='form')
        form2 = UpdateCustomerFormTwo(request.POST,instance=request.user.userprofile, prefix='form2')

        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return redirect(reverse('main:customer_profile'))
        else:
            return render(request,'main/customer_profile.html',{'form':form, 'form2':form2})
    else:
        form = UpdateCustomerForm(instance = request.user,prefix='form')
        form2 = UpdateCustomerFormTwo(instance = request.user.userprofile,prefix='form2')
        args = {'form':form,'form2':form2}
        return render(request,'main/customer_profile.html',args)




def change_password(request):
    
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user = request.user)
        if form.is_valid():
            form.save()
            messages.success(request,"Your new password has been saved")
            update_session_auth_hash(request,form.user)
            return redirect(reverse('main:profile'))

    else:
        form = PasswordChangeForm(user=request.user)
    args = {'form':form}
    return render(request,'main/change_password.html', args)     



# def login_page(request):
#     form = LoginForm(request.POST or None)
#     context = {
#         "form": form
#     }
    
#     next_ = request.GET.get('next')
#     next_post = request.POST.get('next')
#     redirect_path = next_ or next_post or None
#     if form.is_valid():
#         print(form.cleaned_data)
#         email  = form.cleaned_data.get("email")
#         password  = form.cleaned_data.get("password")
#         user = authenticate(request, email=email, password=password)
#         if user is not None:
            
#             login(request, user)
            
#             if is_safe_url(redirect_path, request.get_host()):
#                 return redirect(redirect_path)
#             else:
#                 return redirect("/")
           
#         else:
#             # Return an 'invalid login' error message.
#             print("Error")

#     return render(request, "main/login.html", context)

class LoginView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'main/login.html'

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        email  = form.cleaned_data.get("email")
        password  = form.cleaned_data.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            user_logged_in.send(user.__class__, instance=user, request=request)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        return super(LoginView, self).form_invalid(form)

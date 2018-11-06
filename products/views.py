from django.views.generic import ListView, DetailView, TemplateView
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import Product, Category, SubCategory, SubSubCategory
from cart.models import Cart
from analytics.mixin import ObjectViewedMixin
from django.db.models import Count
from random import randint
from random import shuffle
# Create your views here.
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count




class ProductFeaturedListView(ListView):
    # queryset = Product.objects.all()
    template_name = "products/product_featured_list.html"


    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().featured()

   
    
class ProductFeaturedDetailView(ObjectViewedMixin, DetailView):
    # queryset = Product.objects.all().featured()
    template_name = "products/product_featured_details.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().featured()
    


class ProductListView(TemplateView):
    
    template_name = "products/product_list.html"
    
    def get_context_data(self, *args, **kwargs):
        # context = super(ProductListView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        product_list = list(Product.objects.all())
        shuffle(product_list)
        paginator = Paginator(product_list, 18)
        page = self.request.GET.get('page')

        category      = Category.objects.all()[:7]

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        

        context = { 'products':products,
                    'cart': cart_obj,
                    'category': category }

        print(products)
        return context
    

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     cart_obj, new_obj = Cart.objects.new_or_get(self.request)
    #     category      = Category.objects.all()[:7]

    #     context['cart'] = cart_obj
    #     return context


    

class ProductDetailSlugView(DetailView):
    queryset = Product.objects.all()
    template_name = "products/product_details.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        featured_product = list(Product.objects.filter(featured = True))[:2]
        shuffle(featured_product)
        context['cart'] = cart_obj
        context['featured_product'] = featured_product
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        #instance = get_object_or_404(Product, slug=slug, active=True)
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("Not found..")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("wtf ")
        return instance
    
    
# class ProductCategoryListView(ListView):
#     template_name = "products/product_category_listview.html"
#     queryset      = Category.objects.all()[:6]



def get_brand(request,slug):
    pass      

def get_category(request, slug):
    category_product_list = list(Product.objects.filter(category__slug=slug))

    subcategory = SubCategory.objects.filter(category__slug=slug)
    category_name   = Category.objects.filter(slug = slug)[:1]

    shuffle(category_product_list)
    paginator = Paginator(category_product_list, 1)
    page = request.GET.get('page')

    try:
        category_product = paginator.page(page)
    except PageNotAnInteger:
        category_product = paginator.page(1)
    except EmptyPage:
        category_product = paginator.page(paginator.num_pages)


    context = {'category_product' : category_product, 
                'sub_category':subcategory,
                'category_name':category_name}
    return render(request,'products/product_category_detailview.html', context)


def get_sub_category(request, slug, sub_slug):
    sub_name = SubCategory.objects.filter(category__slug=slug, slug = sub_slug)[:1]
    sub_category_product_list = list(Product.objects.filter(category__slug=slug, subcategory__slug = sub_slug))
    shuffle(sub_category_product_list)
    paginator = Paginator(sub_category_product_list, 1)
    page = request.GET.get('page')

    try:
        sub_category_product = paginator.page(page)
    except PageNotAnInteger:
        sub_category_product = paginator.page(1)
    except EmptyPage:
        sub_category_product = paginator.page(paginator.num_pages)


    subcategory_name = SubSubCategory.objects.filter(category__slug=slug, subcategory__slug = sub_slug)
    context = {  'sub_category_product' : sub_category_product , 
                 'subcategory_name' : subcategory_name,
                 'sub_name':sub_name}
    return render(request, 'products/product_subcategory_detailview.html',context)


def get_sub_sub_category(request, slug, sub_slug, subsub_slug):
    subsub_category_product_list = list(Product.objects.filter(category__slug=slug, subcategory__slug = sub_slug, subsubcategory__slug = subsub_slug))
    shuffle(subsub_category_product_list)
    paginator = Paginator(subsub_category_product_list, 1)
    page = request.GET.get('page')

    try:
        subsub_category_product = paginator.page(page)
    except PageNotAnInteger:
        subsub_category_product = paginator.page(1)
    except EmptyPage:
        subsub_category_product = paginator.page(paginator.num_pages)



    subcategory_name = SubCategory.objects.filter(category__slug=slug)
    subsub_name = SubSubCategory.objects.filter(category__slug=slug, subcategory__slug = sub_slug, slug = subsub_slug)[:1]
    context = {  'subsub_category_product' : subsub_category_product , 
                'subcategory_name' : subcategory_name,
                'subsub_name':subsub_name}
    return render(request, 'products/product_subsubcategory_detailview.html',context)

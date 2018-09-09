from django.views.generic import ListView, DetailView
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import Product, Category, SubCategory
from cart.models import Cart
from analytics.mixin import ObjectViewedMixin

# Create your views here.




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
    


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = "products/product_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context


    
# class ProductDetailView(DetailView):
#     queryset = Product.objects.all()
#     template_name = "products/product_details.html"


#     def get_context_data(self, *args,**kwargs):
#         context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
#         return context
    
#     def get_object(self, *args, **kwargs):
#         request = self.request
#         pk = self.kwargs.get('pk')
#         instance = Product.objects.get_by_id(pk)
#         if instance is None :
#             raise Http404("Product doest not exist")
#         return instance

# class ProductDetailSlugView(ObjectViewedMixin, DetailView):

class ProductDetailSlugView(DetailView):
    queryset = Product.objects.all()
    template_name = "products/product_details.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
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
    
    
class ProductCategoryListView(ListView):
    template_name = "products/product_category_listview.html"
    queryset      = Category.objects.all()[:6]


# class ProductCategoryDetailView(DetailView):
    
#     template_name = "products/product_category_detailview.html"
#     def get_object(self,*args, **kwargs):
        
#         request = self.request
#         slug = self.kwargs.get('slug')
#         #instance = get_object_or_404(Product, slug=slug, active=True)
#         instance = Product.objects.filter(category__slug=slug)
#         print(instance)
#         # try:
            
#         # except Category.DoesNotExist:
#         #     raise Http404("Not found..")
#         # # except Product.MultipleObjectsReturned:
#         # #     qs = Product.objects.filter(slug=slug, active=True)
#         # #     instance = qs.first()
#         # except:
#         #     raise Http404("wtf ")
#         context['instance'] = instance
#         return context
        

def get_category(request, slug):
    category_name = Product.objects.filter(category__slug=slug)
    subcategory_name = SubCategory.objects.filter(category__slug=slug)
    print(category_name)
    print(subcategory_name)
    queryset   = Category.objects.filter(slug = category_name)
    context = {'category' : category_name, 'sub_category':subcategory_name}
    return render(request,'products/product_category_detailview.html', context)


def get_sub_category(request, slug, sub_slug):
    sub_category_product = Product.objects.filter(category__slug=slug, subcategory__slug = sub_slug)
    subcategory_name = SubCategory.objects.filter(category__slug=slug)
    context = {  'sub_category_product' : sub_category_product , 'subcategory_name' : subcategory_name}
    return render(request, 'products/product_subcategory_detailview.html',context)


from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from products.models import Product

# Create your views here.



class SearchProductListView(ListView):
    # queryset = Product.objects.all()
    template_name = "search/search_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(SearchProductListView, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        # SearchQuery.objects.create(query=query)
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q', None) # method_dict['q']
        if query is not None:
            # lookups = Q(title__icontains=query) | Q(description__icontains=query)
            return Product.objects.search(query)
        return Product.objects.featured()
        '''
        __icontains = field contains this
        __iexact = fields is exactly this
        '''

# class CategoryListView(ListView):
#     template_name = "search/category_list.html"     

#     def get_context_data(self,*args, **kwargs):
#         con
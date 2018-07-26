from django.conf.urls import url

from products import views
from products.views import (
        ProductListView,
        # ProductDetailView,
        ProductFeaturedListView,
        ProductFeaturedDetailView,
        ProductDetailSlugView
        
        )

app_name = 'product'


urlpatterns =[
     url(r'^$',ProductListView.as_view(),name='product-view'),
#      url(r'^/(?P<pk>\d+)/$',ProductDetailView.as_view(),name='product-details'),
     
     url(r'^(?P<slug>[\w-]+)/$',ProductDetailSlugView.as_view(),name='product-details'),

     url(r'^featured/$',ProductFeaturedListView.as_view(),name='product-featured-view'),
     url(r'^featured/details/(?P<pk>\d+)/$',ProductFeaturedDetailView.as_view(),name='product-featured-details'),
     
]
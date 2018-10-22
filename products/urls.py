from django.conf.urls import url

from products import views
from products.views import (
        ProductListView,
        # ProductDetailView,
        ProductFeaturedListView,
        ProductFeaturedDetailView,
        ProductDetailSlugView,
        ProductCategoryListView,
        # ProductCategoryDetailView,
        
        )

app_name = 'product'


urlpatterns =[
     url(r'^$',ProductListView.as_view(),name='product-view'),
#      url(r'^/(?P<pk>\d+)/$',ProductDetailView.as_view(),name='product-details'),
     
     url(r'^(?P<slug>[\w-]+)/$',ProductDetailSlugView.as_view(),name='product-details'),

     url(r'^featured/$',ProductFeaturedListView.as_view(),name='product-featured-view'),
     url(r'^featured/details/(?P<pk>\d+)/$',ProductFeaturedDetailView.as_view(),name='product-featured-details'),
     
     url(r'^category/$', ProductCategoryListView.as_view(), name='category-list'),
#      url(r'^category/(?P<slug>[\w-]+)/$', ProductCategoryDetailView.as_view(), name='category-detail'),
     url(r'^category/(?P<slug>[\w-]+)/$', views.get_category, name='category-detail'),
     url(r'^category/(?P<slug>[\w-]+)/(?P<sub_slug>[\w-]+)/$', views.get_sub_category, name='subcategory-detail'),
     url(r'^category/(?P<slug>[\w-]+)/(?P<sub_slug>[\w-]+)/(?P<subsub_slug>[\w-]+)/$', views.get_sub_sub_category, name='subsubcategory-detail'),
     url(r'^brand/(?P<slug>[\w-]+)/$', views.get_brand, name='brand-detail'),

]
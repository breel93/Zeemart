from django.conf.urls import url

from products import views
from search.views import SearchProductListView

app_name = 'search'


urlpatterns =[
     url(r'^$',SearchProductListView.as_view(),name='search-query'),
#      url(r'^/(?P<pk>\d+)/$',ProductDetailView.as_view(),name='product-details'),
     
]
from django.conf.urls import url

from products import views
from .views import cart_home, cart_update, checkout_home, checkout_done_view

app_name = 'cart'


urlpatterns =[
    url(r'^$',cart_home,name='home'),
#      url(r'^/(?P<pk>\d+)/$',ProductDetailView.as_view(),name='product-details'),
    url(r'^update/$',cart_update,name='update'),

    url(r'^checkout/success/$', checkout_done_view, name='success'),

    url(r'^checkout/$',checkout_home, name='checkout'),
]
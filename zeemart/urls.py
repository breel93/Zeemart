"""zeemart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from address.views import checkout_address_create_view, checkout_address_reuse_view
from cart.views import cart_detail_api_view
from marketing.views import MarketingPreferenceUpdateView
from marketing.views import MailchimpWebhookView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('main.urls', namespace='main')),
    url(r'^products/', include('products.urls', namespace='product')),
    url(r'^search/', include('search.urls', namespace='search')),
    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^checkout/address/create/$', checkout_address_create_view, name='checkout_address_create'),
    url(r'^checkout/address/reuse/$', checkout_address_reuse_view, name='checkout_address_reuse'),
    url(r'^api/cart/$', cart_detail_api_view, name='api-cart'),
    url(r'^settings/email/$', MarketingPreferenceUpdateView.as_view(), name='marketing-pref'),
    url(r'^webhooks/mailchimp/$', MailchimpWebhookView.as_view(), name='webhooks-mailchimp'),
    # url(r'^order/', include('order.urls', namespace='order')),
   
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
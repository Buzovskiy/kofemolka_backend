"""
URL configuration for kofemolka_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path, include
from sms.views import send_sms_view, check_sms_code
from app_settings.views import get_settings, get_settings_list
from product.views import get_products_list, get_product, get_batch_ticket, products_exchange

urlpatterns = [
    path('admin/', admin.site.urls),

    path('v1/users/send-sms/api_token=<str:api_token>', send_sms_view),
    path('v1/users/check-sms-code/api_token=<str:api_token>', check_sms_code),

    path('v1/appsettings/get-settings/api_token=<str:api_token>', get_settings),
    path('v1/appsettings/get-settings-list/api_token=<str:api_token>', get_settings_list),

    path('v1/products/get-products-list/api_token=<str:api_token>', get_products_list),
    path('v1/products/get-product/product_id=<int:product_id>/api_token=<str:api_token>', get_product),
    path('v1/products/get-batchticket/product_id=<int:product_id>/api_token=<str:api_token>', get_batch_ticket),
    path('v1/products/products-exchange/api_token=<str:api_token>', products_exchange),
]

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

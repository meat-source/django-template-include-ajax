from django.contrib import admin
from django.urls import path
from app.views import demo,include_ajax

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', demo),
    path('include-ajax/<template>', include_ajax),
]

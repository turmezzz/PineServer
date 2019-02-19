from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^', include('pineapp.urls'))
]

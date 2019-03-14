from django.contrib import admin
import os
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

urlpatterns = [
    url(r'admin/', admin.site.urls),
    url(r'^', include('MainApp.urls'))
]
urlpatterns += static('../MainApp/files/zips', document_root=os.path.join(settings.BASE_DIR, 'reports'))

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^login', views.login, name='login'),
    url(r'^signup', views.signup, name='signup'),
    url(r'^home', views.home, name='home'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^info', views.info, name='info'),
    url(r'^about', views.about, name='about'),
    url(r'^contact', views.contact, name='contact'),
    url(r'^download_.+', views.download, name='download')
]


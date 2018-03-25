from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$',views.main, name = 'main'),
    url(r'^regist/$',views.regist),
    url(r'^checkuserid/$', views.checkuserid),
    url(r'^login/$', views.login,name = 'login'),
    url(r'^quit/$', views.quit),
    url(r'^verifycode/$', views.verifycode),
    url(r'^forgetpassword/$', views.forgetpassword),
    url(r'^forget_checkuserid/$', views.forget_checkuserid),
]

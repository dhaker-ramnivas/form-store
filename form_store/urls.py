from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^form$',views.insertForm, name='store_form'),
    url(r'^form/$',views.updateForm, name='store_update_form'),
    url(r'^form/list$',views.getList, name='store_get_forms'),
    url(r'^form/get/(?P<form_id>\w{0,50})/$',views.getFormById, name='store_get_form_by_id'),
    url(r'^form/getname/(?P<form_name>\w{0,50})/$',views.getFormByName, name='store_get_form_by_id'),
    ]
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^form$', views.DataStore.as_view(), name='store_data'),

    ]
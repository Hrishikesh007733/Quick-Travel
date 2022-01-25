from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views  
 
urlpatterns = [
    path('', views.index, name='index'),  
    path('about', views.about, name='about'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('manager', views.manager, name='manager'),
    path('add_package', views.add_package, name='add_package'),
    path('add_destination', views.add_destination, name='add_destination'),
    path('manager_home', views.manager_home, name='manager_home'),
    path('edit_desti/<str:pk>', views.edit_desti, name='edit_desti'),
    path('delete_product/<str:pk>', views.deleteProduct, name='delete_prod'),
    path('manager_pack', views.manager_pack, name='manager_pack'),
    path('edit_pacakage/<str:dest_name>', views.edit_pacakage, name='edit_pacakage'),
    path('delete_product1/<str:dest_name>', views.deleteProduct1, name='delete_prod1'),
    path('logout', views.logout, name='logout'),
    path('search', views.search, name='search'),
    path('destination_list/<str:city_name>', views.destination_list, name='destination_list'),
    path('destination_list/destination_details/<str:city_name>', views.destination_details, name='destination_details'),
    path('destination_details/<str:city_name>', views.destination_details, name='destination_details'),
    path('destination_list/destination_details/pessanger_detail_def/<str:city_name>',views.pessanger_detail_def,name='pessanger_detail_def'),
    path('upcoming_trips', views.upcoming_trips, name='upcoming_trips'),
    path('delete_uptrip/<str:first_name>', views.delete_uptrip, name='delete_uptrip'),
    path('destination_list/destination_details/pessanger_detail_def/pessanger_detail_def/card_payment', views.card_payment, name='card_payment'),
]
 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
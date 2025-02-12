from django.urls import path
from . import views
urlpatterns = [
    path('', views.home_page, name='homepage'),
    path('polling-unit/<int:polling_unit_id>/', views.individual_polling, name='polling_unit'),
    path('lga-result/', views.lga_results, name='lga-result'),
    path('add-polling-unit-results/', views.add_polling_unit_results, name='add_polling_unit_results'),
    path('get_polling_units/', views.get_polling_units, name='get_polling_units'), 
    path('success_page/', views.success_page, name='success_page'), 
]
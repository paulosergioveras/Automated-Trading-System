from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_stocks, name='search'),
    path('results/', views.results_stocks, name='results'),
]

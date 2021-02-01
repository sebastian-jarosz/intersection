from django.urls import path
from . import views

app_name = 'segments'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('check_intersection/', views.check_intersection, name='check_intersection'),
    path('<int:pk>/', views.ResultView.as_view(), name='result')
]

from django.urls import path
from . import views

app_name = 'segments'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('check_intersection/', views.check_intersection, name='check_intersection'),
    path('<int:pk>/result/', views.ChartResultView.as_view(), name='result'),
    path('<int:pk>/', views.ChartResultJSONView.as_view(), name='result_json'),
]

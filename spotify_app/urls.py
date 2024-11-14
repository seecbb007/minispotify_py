from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page_view, name='main_page_view'),  # Ensure the name matches your template
    path('dashboard/', views.main_page_view, name='dashboard'),
   
    path('analyze/', views.analyze_image_view, name='analyze_image'),  # Add URL pattern for analyze image
]

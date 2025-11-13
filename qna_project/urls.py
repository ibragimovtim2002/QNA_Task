from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('questions.api_urls')),  # API
    path('', include('questions.urls')),         # Главная страница
]
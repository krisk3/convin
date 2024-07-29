"""
URL configuration for app project.
"""

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path("admin/", admin.site.urls), # Access admin panel
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'), # Download API schema file
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'), # API documentation
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'), # API ReDocs documentation
    path('api/user/', include('user.urls')), # User APIs
    path('api/expense/', include('expense.urls')), # Expense APIs
]


admin.site.site_header = 'Convin'
admin.site.index_title= 'Admin Panel'
admin.site.site_title = 'Convin Admin Panel'

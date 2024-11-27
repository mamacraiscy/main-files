from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ctu_scheduler/', include('scheduling_system.urls')),  # Base path for your app
]

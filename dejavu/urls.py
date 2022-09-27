from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('baseball/', include('baseball.urls')),
    path('', RedirectView.as_view(url='baseball/')),

] 

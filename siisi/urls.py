"""
URL configuration for wahou project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language

from django.contrib import admin
from django.urls import path,  include
from two_factor.urls import urlpatterns as tf_urls

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(tf_urls)),  # Include 2FA URLs
    path('', include('two_factor_auth.urls')),
    path('', include('chatgpt.urls')),
    path('', include('base.urls')),
    path('', include('chat_forum.urls')), 
    #path('api', include('base.api.urls')),
]

urlpatterns += i18n_patterns(
    # Translated URLs
    path('set_language/', set_language, name='set_language'),
)

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

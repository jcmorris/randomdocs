from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from randomdocs.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TechDocListView.as_view(), name='display_feed'),
    path('api/tech-docs/', TechDocListViewAPI.as_view(), name='api_tech_docs_list'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns



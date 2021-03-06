from django.conf import settings
from django.conf.urls import include, url
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import logout
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from project_structure import urls as project_structure_urls
from home import views as home_views

from search import views as search_views



urlpatterns = [
    url(r'^django-admin/', admin.site.urls),
    url(r'^publications/', include('publications_bootstrap.urls')),
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^project/', include(project_structure_urls)),
    url(r'^search/$', search_views.search, name='search'),
    url(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    url(r'^login/$', home_views.login_redirect, name='login'),
    path(r'update/<int:pk>/', home_views.UpdateProfile.as_view(), name='update-profile'),
    url(r'^$', home_views.login_redirect, name='index'),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r'', include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r'^pages/', include(wagtail_urls)),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

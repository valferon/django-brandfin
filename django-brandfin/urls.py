from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    # Examples:
    # url(r'^$', 'django-brandfin.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('brandfin.urls')),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )

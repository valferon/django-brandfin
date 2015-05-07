SECRET_KEY = 'shhh'
SITE_ID = 1

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

ROOT_URLCONF = 'brandfin.tests.urls'

EXPLORER_TRANSFORMS = (
    ('foo', '<a href="{0}">{0}</a>'),
    ('bar', 'x: {0}')
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.static",
    "django.core.context_processors.request",
)

TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.filesystem.Loader',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'brandfin',
)

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
)

STATIC_URL = '/static/'

MIDDLEWARE_CLASSES = ('django.contrib.sessions.middleware.SessionMiddleware',
                      'django.contrib.auth.middleware.AuthenticationMiddleware')

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

EXPLORER_USER_QUERY_VIEWS = {}

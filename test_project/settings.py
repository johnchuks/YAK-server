"""
Django settings for test project for YAK-server

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'N/A'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'oauth2_provider',
    'rest_framework',
    'social.apps.django_app.default',

    'rest_user',
    'rest_social',
    'rest_notifications',
    'test_app',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'test_project.urls'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

USER_APP_LABEL = 'test_app'
USER_MODEL = 'user'
AUTH_USER_MODEL = "{}.{}".format(USER_APP_LABEL, USER_MODEL.capitalize())
USER_SERIALIZER = "test_app.api.serializers.ProjectUserSerializer"

PACKAGES_TO_TEST = ['test_project',
                    'rest_core',
                    'rest_social',
                    'rest_notifications',
                    'rest_user']

API_SCHEMA = 'test_project/api-schema-1.0.json'

AUTHENTICATION_BACKENDS = (
    "social.backends.facebook.Facebook2OAuth2",
    "social.backends.twitter.TwitterOAuth",
    "rest_user.backends.CaseInsensitiveMezzanineBackend",
)

SOCIAL_AUTH_FACEBOOK_KEY = ''
SOCIAL_AUTH_FACEBOOK_SECRET = ''
SOCIAL_AUTH_FACEBOOK_APP_TOKEN = ''
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'publish_actions', 'user_about_me', 'user_location']

SOCIAL_SHARE_DELAY = 60

USE_FACEBOOK_OG = True
FACEBOOK_OG_NAMESPACE = ""

SOCIAL_AUTH_TWITTER_KEY = ''
SOCIAL_AUTH_TWITTER_SECRET = ''

SOCIAL_AUTH_PIPELINE = (
    # Get the information we can about the user and return it in a simple
    # format to create the user instance later. On some cases the details are
    # already part of the auth response from the provider, but sometimes this
    # could hit a provider API.
    'social.pipeline.social_auth.social_details',

    # Get the social uid from whichever service we're authing thru. The uid is
    # the unique identifier of the given user in the provider.
    'social.pipeline.social_auth.social_uid',

    # Verifies that the current auth process is valid within the current
    # project, this is were emails and domains whitelists are applied (if
    # defined).
    'social.pipeline.social_auth.auth_allowed',

    # If used, replaces default 'social.pipeline.social_auth.social_user'
    # 'rest_social.rest_social.pipeline.social_auth_user',

    # Checks if the current social-account is already associated in the site.
    'social.pipeline.social_auth.social_user',

    # Make up a username for this person, appends a random string at the end if
    # there's any collision.
    'social.pipeline.user.get_username',

    # Send a validation email to the user to verify its email address.
    # Disabled by default.
    # 'social.pipeline.mail.mail_validation',

    # Associates the current social details with another user account with
    # a similar email address. Disabled by default.
    'social.pipeline.social_auth.associate_by_email',

    # Create a user account if we haven't found one yet.
    'social.pipeline.user.create_user',

    # Create the record that associated the social account with this user.
    'social.pipeline.social_auth.associate_user',

    # Populate the extra_data field in the social record with the values
    # specified by settings (and the default ones like access_token, etc).
    'social.pipeline.social_auth.load_extra_data',

    # Update the user record with any changed info from the auth service.
    'social.pipeline.user.user_details',

    'rest_social.rest_social.pipeline.save_extra_data',
    'rest_social.rest_social.pipeline.get_profile_image',
)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_core.permissions.IsOwnerOrReadOnly',
    ),
    'PAGINATE_BY': 20,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter'
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'}
}

ACCESS_TOKEN_EXPIRE_SECONDS = 7776000  # 90 days

SOCIAL_MODEL = "test_app.Post"
SOCIAL_MODEL_FACTORY = "test_app.tests.factories.PostFactory"

SOCIAL_FRIEND_ACTIONS = (
    (0, 'follow', 'is following'),
    (1, 'like', 'favorited a post'),
    (2, 'reply', 'replied to a post')
)

NOTIFICATION_TYPES = (
    (0, 'follow', 'follow.html'),
    (1, 'like', 'like.html'),
    (2, 'comment', 'comment.html'),
    (3, 'mention', 'mention.html'),
    (4, 'share', 'share.html'),
)
EMAIL_NOTIFICATION_SUBJECT = 'Test Project Notification'

PUSHWOOSH_AUTH_TOKEN = ""
PUSHWOOSH_APP_CODE = ""

USER_EXTRA_FIELDS = ['image', 'about', 'type']


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

try:
    from local_settings import *
except ImportError:
    pass
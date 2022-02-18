from smart_iam.settings.development import *  # noqa

TEST_RUNNER = "xmlrunner.extra.djangotestrunner.XMLTestRunner"
TEST_OUTPUT_DIR = "./reports/"
TEST_OUTPUT_FILENAME = "unit.xml"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "test_db.sqlite3",  # noqa
    }
}

INSTALLED_APPS += ["behave_django"]  # noqa

DEBUG = False

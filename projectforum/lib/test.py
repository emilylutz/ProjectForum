from django.conf import settings
from django.test import LiveServerTestCase

from functools import wraps


try:
    web_drivers = settings.SELENIUM_WEBDRIVER_MODULES
except AttributeError:
    from selenium import webdriver
    web_drivers = [
        webdriver.Chrome,
        # webdriver.Edge,
        # webdriver.Firefox,
        # webdriver.Ie,
        # webdriver.Opera,
        # webdriver.Safari,
    ]


def wrap_with_drivers():
    def wrapper(func):
        func.wrap_with_drivers = None
        return func
    return wrapper


def method_wrapper(func, driver):
    @wraps(func)
    def wrapped(self, *args, **kwargs):
        if self.driver is not None:
            self.fail('Driver improperly cleaned up in previous test. Did you '
                      'override tearDown without calling the superclass '
                      'implementation?')
        self.driver = driver()
        return func(self, *args, **kwargs)
    return wrapped


class WebDriverWrapper(type):
    """
    Metaclass that wraps the appropriate methods to use the right web driver.
    """

    def __new__(cls, name, bases, attr):
        wrapped_methods = {}
        for method_name in attr:
            if hasattr(attr[method_name], "wrap_with_drivers"):
                source = attr[method_name]
                source_name = method_name.lstrip("_")
                    
                for wd in web_drivers:
                    webdriver_name = wd.__module__.split('.')[-2]
                    method = method_wrapper(source, wd)
                    method.__name__ = "%s_%s" % (source_name, webdriver_name)
                    wrapped_methods[method.__name__] = method

        attr.update(wrapped_methods)
        return type(name, bases, attr)


class SeleniumTestCase(LiveServerTestCase):
    """
    A base test case for Selenium. Wraps methods with the @wrap_with_drivers
    decorator to run with the drivers specified in the settings file in
    settings.SELENIUM_WEBDRIVER_MODULES. If this is not set, it uses a default
    list of Chrome, Edge, Firefox, Ie, Opera, and Safari. Name the test that
    is to be wrapped with a leading underscore so that it will only be run
    when wrapped. Inside the test, you can access the driver through the
    field `self.driver`. Make sure you call super.teardown if you override it
    so that the driver is properly destructed.
    
    Make sure you use the WebDriverWrapper metaclass.

    Provides helper methods for common actions.
    """

    def __init__(self, *args, **kwargs):
        self.driver = None
        super(SeleniumTestCase, self).__init__(*args, **kwargs)

    def tearDown(self):
        if self.driver is not None:
            self.driver.quit()
            self.driver = None

    def open(self, url):
        self.driver.get("%s%s" % (self.live_server_url, url))

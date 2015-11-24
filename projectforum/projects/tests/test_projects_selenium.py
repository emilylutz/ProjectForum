from django.core.urlresolvers import reverse

from projectforum.lib.test import (
    SeleniumTestCase,
    WebDriverWrapper,
    wrap_with_drivers,
)


class ProjectsSeleniumTest(SeleniumTestCase):

    __metaclass__ = WebDriverWrapper

    @wrap_with_drivers()
    def _test_that_selenium_tests_work(self):
        print('2')

    @wrap_with_drivers()
    def _test_that_selenium_index_loads(self):
        print('3')
        self.open(reverse('index'))

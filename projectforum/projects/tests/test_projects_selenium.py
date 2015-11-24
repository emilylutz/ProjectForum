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

    @wrap_with_drivers()
    def _test_header_links_work(self):
        #home, about, projects, view all projects, create new project, about
        #login
        #then once logged in:
        #username, view profile, change password, log out
        pass

    @wrap_with_drivers()
    def _test_that_user_can_view_list_of_projects(self):
        pass

    @wrap_with_drivers()
    def _test_that_user_can_log_in(self):
        pass

    @wrap_with_drivers()
    def _test_that_user_can_log_out(self):
        pass

    @wrap_with_drivers()
    def _test_that_user_can_change_password(self):
        pass



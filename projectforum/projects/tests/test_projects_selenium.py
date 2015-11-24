from django.core.urlresolvers import reverse

from projectforum.lib.test import (
    SeleniumTestCase,
    WebDriverWrapper,
    wrap_with_drivers,
)


class ProjectsSeleniumTest(SeleniumTestCase):

    __metaclass__ = WebDriverWrapper

    @wrap_with_drivers()
    def _test_that_selenium_index_loads(self):
        print('3')
        self.open(reverse('index'))
        logo = self.driver.find_element_by_id("headerLogo")
        self.assertIn('Project Forum', logo.text)

    @wrap_with_drivers()
    def _test_header_links_work(self):
        self.open(reverse('index'))
        #Test home tab
        homeTab = self.driver.find_element_by_id("home-tab")
        homeTab.click()
        location = self.driver.get_location()
        print location
        self.assertEqual('/', location)
        #Test projects tab
        projectsTab = self.driver.find_element_by_id("projects-tab")
        projectsTab.click()
        location = self.driver.get_location()
        print location
        self.assertEqual('/projects/list', location)
        #move_to_element
        #home, about, projects, view all projects, create new project, about
        #login
        #then once logged in:
        #username, view profile, change password, log out
        pass

    # @wrap_with_drivers()
    # def _test_that_user_can_log_in(self):
    #     pass

    # @wrap_with_drivers()
    # def _test_that_user_can_log_out(self):
    #     pass

    # @wrap_with_drivers()
    # def _test_that_user_can_change_password(self):
    #     pass

    # @wrap_with_drivers()
    # def _test_registration_if_you_can(self):
    #     pass

    @wrap_with_drivers()
    def _test_that_user_can_view_list_of_projects(self):
        #check for specific project titles and descriptions
        #try filtering them various ways
        pass






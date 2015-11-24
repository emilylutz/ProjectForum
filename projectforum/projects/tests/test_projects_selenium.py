from django.core.urlresolvers import reverse

from projectforum.lib.test import (
    SeleniumTestCase,
    WebDriverWrapper,
    wrap_with_drivers,
)

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from projectforum.projects.models import Project


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
        self.assertTrue(homeTab.is_displayed())
        homeTab.click()
        location = self.driver.current_url
        self.assertEqual(self.format_url('/'), location)

        #Test projects tab
        projectsTab = self.driver.find_element_by_id("projects-tab")
        self.assertTrue(projectsTab.is_displayed())
        projectsTab.click()
        location = self.driver.current_url
        self.assertEqual(self.format_url('/project/list/'), location)

        #Test about tab
        aboutTab = self.driver.find_element_by_id("about-tab")
        self.assertIsNotNone(aboutTab)
        self.assertTrue(aboutTab.is_displayed())
        aboutTab.click()
        location = self.driver.current_url
        self.assertEqual(self.format_url('/about/'), location)

        # #Test hovering works to view all projects
        # print "Doing the thing!"
        # projectsTab = self.driver.find_element_by_id("projects-tab")
        # viewAllProjectsTab = self.driver.find_element_by_id("view-all-projects-tab")
        # self.assertFalse(viewAllProjectsTab.is_displayed())
        # actions = ActionChains(self.driver).move_to_element(projectsTab).perform()
        # print "Did the hover. Waiting 10 seconds"
        # self.driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
        # # click(viewAllProjectsTab)
        # # actions.perform()
        # self.assertTrue(viewAllProjectsTab.is_displayed())
        # viewAllProjectsTab.click()
        # location = self.driver.current_url
        # self.assertEqual(self.format_url('/project/list/'), location)

        # #Test hovering works to view all projects
        # projectsTab = self.driver.find_element_by_id("projects-tab")
        # createProjectTab = self.driver.find_element_by_id("create-new-project-tab")
        # self.assertFalse(createProjectTab.is_displayed())
        # ActionChains(self.driver).move_to_element(projectsTab).perform()
        # self.assertTrue(createProjectTab.is_displayed())
        # createProjectTab.click()
        # location = self.driver.current_url
        # self.assertEqual(self.format_url('/project/create/'), location)

        #Test login tab
        loginTab = self.driver.find_element_by_id("login-tab")
        self.assertTrue(loginTab.is_displayed())
        loginTab.click()
        location = self.driver.current_url
        self.assertEqual(self.format_url('/profile/login/'), location)



    # @wrap_with_drivers()
    # def _test_mobile_header_links_work(self):
    #     pass

    @wrap_with_drivers()
    def _test_that_user_can_log_in(self):
        self.open(reverse('profile:login'))

        # input some bad password
        self.driver.find_element_by_id('id_username').send_keys('joe')
        self.driver.find_element_by_id('id_password').send_keys('not_my_password')

        #Test errors correctly
        self.driver.find_element_by_id('id_login_submit').click()
        errors = self.driver.find_element_by_class_name('errorlist')
        self.assertIn("Please enter a correct username and password", errors.text)

        self.create_user('joe', 'topsecret', 'joe@mail.com')

        self.driver.find_element_by_id('id_password').send_keys('topsecret')
        self.driver.find_element_by_id('id_login_submit').click()

        location = self.driver.current_url
        self.assertEqual(self.format_url('/'), location)

        usernameTab = self.driver.find_element_by_id('username-tab')

        self.assertIn('joe', usernameTab.text)

        #TODO: username, view profile, change password, log out

    # @wrap_with_drivers()
    # def _test_that_user_can_log_out(self):
    #     pass

    # @wrap_with_drivers()
    # def _test_that_user_can_change_password(self):
    #     # uses email!
    #     pass

    # @wrap_with_drivers()
    # def _test_registration_if_you_can(self):
    #     pass

    @wrap_with_drivers()
    def _test_that_user_can_view_list_of_projects(self):
        #Create some projects that will be viewed
        joe = self.create_user('joe', 'secret', 'j@mail.com')
        project1 = Project.objects.create(
            title="Test Title 1",
            description="Test Description 1",
            owner=joe,
            payment=3,
            amount=1,
            status=1,
        )

        project2 = Project.objects.create(
            title="Test Title 2",
            description="Test Description 2",
            owner=joe,
            payment=1,
            amount=2,
            status=1,
        )

        project3 = Project.objects.create(
            title="Test Title 3",
            description="Test Description 3",
            owner=joe,
            payment=2,
            amount=1,
            status=1,
        )

        project4 = Project.objects.create(
            title="Test Title 4",
            description="Test Description 4",
            owner=joe,
            payment=2,
            amount=1,
            status=2,
        )

        self.open(reverse('project:list'))

        #check that all projects with status = 1 are in list
        projectList = self.driver.find_element_by_id('project-list')
        self.assertIn(project1.title, projectList.text)
        self.assertIn(project2.title, projectList.text)
        self.assertIn(project3.title, projectList.text)

        # Projects with status != 1 are not included in list by default
        self.assertNotIn(project4.title, projectList.text)

        #Check that projects link to their pages
        proj1link = self.driver.find_element_by_link_text(project1.title)
        proj1link.click()
        location = self.driver.current_url
        self.assertEqual(self.format_url('/project/'+str(project1.id) + '/'), location)

        self.open(reverse('project:list'))

        proj2link = self.driver.find_element_by_link_text(project2.title)
        proj2link.click()
        location = self.driver.current_url
        self.assertEqual(self.format_url('/project/'+str(project2.id) + '/'), location)

        self.open(reverse('project:list'))

        proj3link = self.driver.find_element_by_link_text(project3.title)
        proj3link.click()
        location = self.driver.current_url
        self.assertEqual(self.format_url('/project/'+str(project3.id) + '/'), location)


    @wrap_with_drivers()
    def _test_that_user_can_filter_list_of_projects(self):
        #Create some projects that will be viewed
        joe = self.create_user('joe', 'secret', 'j@mail.com')
        project1 = Project.objects.create(
            title="Test Title 1",
            description="Test Description 1",
            owner=joe,
            payment=3,
            amount=1,
            status=1,
        )

        project2 = Project.objects.create(
            title="Test Title 2",
            description="Test Description 2",
            owner=joe,
            payment=1,
            amount=2,
            status=1,
        )

        project3 = Project.objects.create(
            title="Test Title 3",
            description="Test Description 3",
            owner=joe,
            payment=2,
            amount=1,
            status=1,
        )

        project4 = Project.objects.create(
            title="Test Title 4",
            description="Test Description 4",
            owner=joe,
            payment=2,
            amount=1,
            status=2,
        )

        self.open(reverse('project:list'))

        # Search for projects with keyword 1
        keywordsInput = self.driver.find_element_by_id('keywords')
        keywordsInput.send_keys('1')
        self.driver.find_element_by_id('button-search').click()

        projectList = self.driver.find_element_by_id('project-list')
        self.assertIn(project1.title, projectList.text)
        self.assertNotIn(project2.title, projectList.text)
        self.assertNotIn(project3.title, projectList.text)
        self.assertNotIn(project4.title, projectList.text)

        #Sort by most recent project
        sortInput = self.driver.find_element_by_class_name('sort-projects')
        sort_options = sortInput.find_elements_by_tag_name("option")

        sort_options[1].click()
        self.driver.find_element_by_id('button-search').click()

        projectList = self.driver.find_element_by_id('project-list')
        projectListItems = projectList.find_elements_by_tag_name("li")

        self.assertIn(project3.title, projectListItems[0].text)
        self.assertIn(project2.title, projectListItems[1].text)
        self.assertIn(project1.title, projectListItems[2].text)

        #Sort by least recent project
        sortInput = self.driver.find_element_by_class_name('sort-projects')
        sort_options = sortInput.find_elements_by_tag_name("option")

        sort_options[2].click()
        self.driver.find_element_by_id('button-search').click()

        projectList = self.driver.find_element_by_id('project-list')
        projectListItems = projectList.find_elements_by_tag_name("li")

        self.assertIn(project1.title, projectListItems[0].text)
        self.assertIn(project2.title, projectListItems[1].text)
        self.assertIn(project3.title, projectListItems[2].text)

    @wrap_with_drivers()
    def _test_project_description_page(self):
        #Create some projects that will be viewed
        joe = self.create_user('joe', 'secret', 'j@mail.com')
        project1 = Project.objects.create(
            title="Test Title 1",
            description="Test Description 1",
            owner=joe,
            payment=3,
            amount=1,
            status=1,
        )

        self.open(reverse('project:detail', args=(project1.id,)))

        titleObject = self.driver.find_element_by_class_name('project_detail_title')
        self.assertIn(project1.title, titleObject.text)

        descriptionObject = self.driver.find_element_by_class_name('project_detail_description')
        self.assertIn(project1.description, descriptionObject.text)

        statusObject = self.driver.find_element_by_class_name('project_status')
        # self.assertIn(project1.get_status_display(), statusObject.text)

        # moreDetailsObject = self.driver.find_element_by_class_name('more_project_details')
        # self.assertIn(project1.owner.username, moreDetailsObject.text)
        # self.assertIn(str(project1.amount), moreDetailsObject.text)
        # self.assertIn(project1.get_payment_display(), moreDetailsObject.text)



        #check for specific project titles and descriptions
        #try filtering them various ways






import pytest
from typing import NoReturn, Final
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException
import pprint
class BasePage(object):

    """
    Base class to initialize the base page that will be called from all pages
    """

    BASE_URL: Final = "http://automationpractice.com/index.php"
    page_uri = ""
    BASE_TITLE: Final = "My Store"
    specific_title = ""

    def __init__(self, driver: WebDriver):
        self._driver = driver
        self.wait_for_page_to_load()
        self._current_url_matches()
        self._title_matches()

    # XPATH locators
    _logo_image_locator = "//img[@class='logo img-responsive']"
    _search_input_locator = "//input[@id='search_query_top']"
    _search_button_locator = "//button[@name='submit_search']"

    # Web elements
    @property
    def logo_image(self) -> WebElement:
        return self._get_element(self._logo_image_locator)

    @property
    def search_input(self) -> WebElement:
        return self._get_element(self._search_input_locator)

    @search_input.setter
    def search_input(self, query: str) -> NoReturn:
        self.search_input.clear()
        self.search_input.send_keys(query)

    @property
    def search_button(self) -> WebElement:
        return self._get_element(self._search_button_locator)

    # Methods
    def _get_element(self, xpath: str) -> WebElement:
        """
        Wait for a element to be present on the screen
        :param xpath: xpath of the element to wait for
        :return: the WebElement
        """
        return self._driver.find_element_by_xpath(xpath)

    def _current_url_matches(self) -> NoReturn:
        """
        Make sure the current url of the page matches the expected title
        :return:
        """
        url = self.BASE_URL + "" if self.page_uri == "" else "?{}".format(self.page_uri)
        current_url = self._driver.current_url
        assert url in current_url, "URL '{0}' not on the current URL of the page ('{1}')".format(url, current_url)

    def _title_matches(self) -> NoReturn:
        """
        Make sure the title of the page matches the expected title
        :return:
        """
        title = "" if self.specific_title == "" else "{} - ".format(self.specific_title) + self.BASE_TITLE
        current_title = self._driver.title
        assert title in current_title, "Name '{0}' not on the title of the page ('{1}')".format(title, current_title)

    def search_product(self, product: str):
        """
        Search for a product
        :param product: name to search by
        :return: a SearchPage instance
        """
        from . import SearchPage    # not a good praxis but it's a way of avoiding circular imports
        self.search_input = product
        self.search_button.click()
        return SearchPage(self._driver)

    def wait_for_page_to_load(self) -> NoReturn:
        """
        Wait for some web elements to show up on the screen
        :return:
        """
        self.logo_image
        self.search_input
class TestBase(object):

    TESTING_URL: Final[str] = "http://automationpractice.com"

    @staticmethod
    @pytest.fixture(scope="function")
    def go_to_base_page(get_driver: WebDriver) -> BasePage:
        """
        Open the browser and go to the Base webpage
        :param get_driver: Selenium driver
        :return: a BasePage instance
        """
        get_driver.get(TestBase.TESTING_URL)
        return BasePage(get_driver)

#def test_this(get_driver):
#    get_driver.get("http://automationpractice.com")
#    get_driver.save_screenshot('/usr/src/app/reports/googlehome.png')
import time
def test_homepage(get_driver):
    #time.sleep(30)
    get_driver.get("http://localhost:80")
    found = False
    for i in get_driver.find_elements(By.XPATH,"//meta[@name='pathname']"):
        if i.get_attribute("content") == "/":
            found = True
    assert found
    get_driver.save_screenshot('/usr/src/app/reports/loadhome.png')


def test_login(get_driver):
    #time.sleep(30)
    get_driver.get("http://localhost:80/login")
    found = False
    for i in get_driver.find_elements(By.XPATH,"//meta[@name='pathname']"):
        if i.get_attribute("content") == "/login":
            found = True
    assert found
    get_driver.save_screenshot('/usr/src/app/reports/login.png')


def test_loginactual(get_driver):
    get_driver.get("http://localhost:80")
    assert get_driver.find_element(By.ID,"userbutton").text == "LOGIN"
    get_driver.find_element(By.ID,"userbutton").click()
    try:
        wait = ui.WebDriverWait(get_driver, 10).until(EC.presence_of_element_located((By.XPATH, "//meta[@name='pathname'][@Content='/login']"))) # timeout after 10 seconds
    except (NoAlertPresentException, TimeoutException) as py_ex:
        pprint.pprint(py_ex)
        assert False
    #get_driver.get("http://localhost:80/login")
    #wait = ui.WebDriverWait(get_driver, 10) # timeout after 10 seconds
    get_driver.find_element(By.ID,"emailinput").send_keys("malcom2073")
    get_driver.find_element(By.ID,"passinput").send_keys(12345)
    get_driver.find_element(By.NAME,"commit").click()
    try:
        wait = ui.WebDriverWait(get_driver, 10).until(EC.presence_of_element_located((By.XPATH, "//meta[@name='pathname'][@Content='/']"))) # timeout after 10 seconds
    except (NoAlertPresentException, TimeoutException) as py_ex:
        pprint.pprint(py_ex)
        assert False
    assert get_driver.find_element(By.ID,"userbutton").text == "MALCOM2073"
    get_driver.find_element(By.ID,"userbutton").click()
    time.sleep(0.5)
    get_driver.find_element(By.ID,"logoutlink").click()
    try:
        
        wait = ui.WebDriverWait(get_driver, 10).until(EC.text_to_be_present_in_element((By.ID,"userbutton"),"LOGIN")) # timeout after 10 seconds
    except (NoAlertPresentException, TimeoutException) as py_ex:
        pprint.pprint(py_ex)
        assert False

    #get_driver.get("http://loadbalancer:80/")
    #results = wait.until(lambda driver: driver.find_element_by_xpath("//meta[@name='pathname']@Content"))
    #for result in results:
    #    print(result.text)
    #    print('-'*80)
    get_driver.save_screenshot('/usr/src/app/reports/loggedin.png')
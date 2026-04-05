from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options 
import os 

options = Options()

# Run in headless mode, so don't actually display the browser window
if 'GITHUB_ENV' in os.environ:
    options.add_argument('--headless')
# Else, running on a local computer, so show browser window. 

class MySeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver(options=options)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_title_in_browser_tab(self):
        self.selenium.get(f"{self.live_server_url}")
        self.assertIn('LMN', self.selenium.title)
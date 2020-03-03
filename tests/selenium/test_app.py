import os
import time

import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import (
    NoSuchElementException,
    WebDriverException)
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from applitools.selenium import Eyes, Target

# Codefresh env vars
hostname = os.getenv('INGRESS_HOSTNAME')
release_name = os.getenv('RELEASE_NAME')
commit_sha = os.getenv('CF_SHORT_REVISION')

# Give Selenium Hub time to start
time.sleep(15)  # TODO: figure how to do this better


# <-- Begin Applitools Visual Testing --> 
eyes = Eyes()
# Set applitools api key
eyes.api_key = os.getenv('APPLITOOLS_API_KEY')
# Set Browser Object for Applitools
browser_name = ip = os.getenv('BROWSER')
browser = webdriver.Remote(
          command_executor='http://selenium_hub:4444/wd/hub',
        #   desired_capabilities=DesiredCapabilities.CHROME
          desired_capabilities={'browserName': browser_name},
)
# Open Eyes         
eyes.open(browser, "Test app", "Croc hunter test-{browser_name}", {'width': 800, 'height': 600})
# Open Browser
browser.get("https://{}".format(hostname))
# Take snapshot
eyes.check("Login Window test", Target.window())
# Close Eyes
eyes.close()
# Quite Browser
browser.quit()
# <-- End Applitools Visual Testing -->


# <-- Begin pytest with Selenium -->
@pytest.fixture(scope='module')
def browser():
    browser_name = ip = os.getenv('BROWSER')
    browser = webdriver.Remote(
        command_executor='http://selenium_hub:4444/wd/hub',
        desired_capabilities={'browserName': browser_name},
    )
    yield browser
    browser.quit()

    
def test_confirm_title(browser):
    browser.get("https://{}".format(hostname))
    assert "Croc Hunter" in browser.title


def test_confirm_canvas_bg(browser):
    browser.get("https://{}".format(hostname))
    element = browser.find_element(By.ID, 'canvasBg')
    assert element.get_attribute('id') == 'canvasBg'


def test_confirm_canvas_enemy(browser):
    browser.get("https://{}".format(hostname))
    element = browser.find_element(By.ID, 'canvasEnemy')
    assert element.get_attribute('id') == 'canvasEnemy'


def test_confirm_canvas_jet(browser):
    browser.get("https://{}".format(hostname))
    element = browser.find_element(By.ID, 'canvasJet')
    assert element.get_attribute('id') == 'canvasJet'


def test_confirm_canvas_hud(browser):
    browser.get("https://{}".format(hostname))
    element = browser.find_element(By.ID, 'canvasHud')
    assert element.get_attribute('id') == 'canvasHud'


def test_confirm_release_name(browser):
    browser.get("https://{}".format(hostname))
    element = browser.find_element(By.XPATH, '//div[@class="details"]')
    assert release_name in element.text


def test_confirm_commit_sha(browser):
    browser.get("https://{}".format(hostname))
    element = browser.find_element(By.XPATH, '//div[@class="details"]')
    assert commit_sha in element.text
# <-- End pytest with Selenium -->

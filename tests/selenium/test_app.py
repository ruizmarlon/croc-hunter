import os
import time

import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import (
    NoSuchElementException,
    WebDriverException)
from applitools.selenium import Eyes, Target

# env vars
hostname = os.getenv('INGRESS_HOSTNAME_DEV')
release_name = os.getenv('RELEASE_NAME')
commit_sha = os.getenv('CF_SHORT_REVISION')

class HelloCrocodiles:

    eyes = Eyes()

    # Initialize the eyes SDK and set your private API key.
    eyes.api_key = os.getenv('APPLITOOLS_API_KEY')

    try:

        # Open a Chrome browser.
        driver = webdriver.Chrome()

        # Start the test and set the browser's viewport size to 800x600.
        eyes.open(driver, "Test app", "First test", {'width': 800, 'height': 600})

        # Navigate the browser to the "hello world!" web-site.
        driver.get(hostname)

        # Visual checkpoint #1.
        eyes.check("First Window test", Target.window())

        # End the test.
        eyes.close()

    finally:

        # Close the browser.
        driver.quit()

        # If the test was aborted before eyes.close was called, ends the test as aborted.
        eyes.abort()

# Give Selenium Hub time to start
time.sleep(15)  # TODO: figure how to do this better

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

"""Selenium WebDriver tests for the login page in login_page/index.html.

Run with a visible browser:  HEADLESS=0 python -m pytest test_login.py -v
Requires Google Chrome; Selenium Manager downloads a matching chromedriver.
"""
import os
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

LOGIN_URL = (Path(__file__).parent / "login_page" / "index.html").resolve().as_uri()
TIMEOUT = 10

# Locators: IDs for the stable form controls, CSS/XPath for the rest.
USERNAME = (By.ID, "username")
PASSWORD = (By.NAME, "password")
LOGIN_BUTTON = (By.CSS_SELECTOR, "form#login-form button[type='submit']")
ERROR_MESSAGE = (By.CSS_SELECTOR, "#error[role='alert']")
WELCOME_HEADING = (By.XPATH, "//section[@id='dashboard']//h1[@id='welcome']")
LOGOUT_BUTTON = (By.ID, "logout-button")


@pytest.fixture
def driver():
    options = Options()
    if os.environ.get("HEADLESS", "1") != "0":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,800")

    browser = webdriver.Chrome(options=options)
    browser.get(LOGIN_URL)
    yield browser
    browser.quit()


def log_in(driver, username, password):
    wait = WebDriverWait(driver, TIMEOUT)
    wait.until(EC.visibility_of_element_located(USERNAME)).send_keys(username)
    driver.find_element(*PASSWORD).send_keys(password)
    wait.until(EC.element_to_be_clickable(LOGIN_BUTTON)).click()


def test_valid_login_shows_dashboard(driver):
    log_in(driver, "student", "Secret@123")

    wait = WebDriverWait(driver, TIMEOUT)
    welcome = wait.until(EC.visibility_of_element_located(WELCOME_HEADING))
    assert welcome.text == "Welcome, student!"
    wait.until(EC.title_contains("Dashboard"))
    # The login form is gone once the user is signed in.
    assert wait.until(EC.invisibility_of_element_located(LOGIN_BUTTON))


@pytest.mark.parametrize(
    "username, password, message",
    [
        ("student", "wrong-password", "Invalid username or password."),
        ("unknown", "Secret@123", "Invalid username or password."),
        ("", "", "Username and password are required."),
        ("student", "", "Username and password are required."),
    ],
)
def test_invalid_login_shows_error(driver, username, password, message):
    log_in(driver, username, password)

    error = WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located(ERROR_MESSAGE)
    )
    assert error.text == message
    # Still on the login page: no dashboard was shown.
    assert not driver.find_element(*WELCOME_HEADING).is_displayed()


def test_logout_returns_to_login_form(driver):
    log_in(driver, "student", "Secret@123")
    wait = WebDriverWait(driver, TIMEOUT)
    wait.until(EC.element_to_be_clickable(LOGOUT_BUTTON)).click()

    wait.until(EC.visibility_of_element_located(USERNAME))
    wait.until(EC.title_contains("Login"))
    assert driver.find_element(*USERNAME).get_attribute("value") == ""

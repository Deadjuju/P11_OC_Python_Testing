import logging
import pprint
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from tests.conftest import client, captured_templates, mocker_clubs
import server


# @pytest.fixture(scope="session")
# def app():
#     app = create_app()
#     multiprocessing.set_start_method("fork")
#     return app
#
#
# @pytest.fixture
# def client(app):
#     return app.test_client()


# chrome_driver_path = 'tests/functional_tests/chromedriver'
chrome_driver_path = r'C:\Users\deadj\code_programmation\OpenClassrooms\PROJET 11 - Améliorez une application Web Python par des tests et du débogage\Projet\P11_OC_Python_Testing\tests\functional_tests\chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)
SERVER_URL = "http://127.0.0.1:5000"


# def test_python_org():
#
#     url = "https://www.python.org/"
#     driver.get(url=url)
#     driver.maximize_window()
#     print("-" * 150)
#     title = driver.title
#     print(title)
#     search_bar = driver.find_element(By.NAME, "q")
#     search_bar.clear()
#     search_bar.send_keys("getting started with python")
#     search_bar.send_keys(Keys.RETURN)
#     print(driver.current_url)
#     time.sleep(2)
#     # driver.close()
#
#     assert title == "Welcome to Python.org"


def test_user_course_buyed_places(mocker):
    valid_mail = "john@simplylift.co"
    url = SERVER_URL + "/"

    mocker.patch.object(server, 'clubs', mocker_clubs)

    # Index
    driver.get(url=url)

    title = driver.find_element(By.TAG_NAME, 'h1').text
    assert "Welcome to the GUDLFT Registration Portal!" in title

    search_bar = driver.find_element(By.NAME, "email")
    search_bar.clear()
    search_bar.send_keys(valid_mail)
    time.sleep(1)
    search_bar.send_keys(Keys.RETURN)

    # show summary
    welcome_message = driver.find_element(By.TAG_NAME, 'h2').text
    assert valid_mail in welcome_message

    club_points_before_transaction = int(driver.find_element(By.CLASS_NAME, 'club-points').text)
    time.sleep(2)

    try:
        book_btn = driver.find_element(By.CLASS_NAME, 'book-places-btn')
    except NoSuchElementException:
        print("Coucou")
    else:
        # book
        book_btn.click()
        expected_url = SERVER_URL + "/book"
        current_url = driver.current_url
        assert expected_url in current_url

        search_bar = driver.find_element(By.NAME, "places")
        search_bar.clear()
        required_places = 1
        search_bar.send_keys(required_places)
        time.sleep(2)
        search_bar.send_keys(Keys.RETURN)

        # check success
        success_message = driver.find_element(By.CLASS_NAME, 'message')
        expected_msg = "Great-booking complete!"
        assert expected_msg in success_message.text

        club_points_after_transaction = int(driver.find_element(By.CLASS_NAME, 'club-points').text)
        assert club_points_before_transaction - club_points_after_transaction == required_places

        # purchasePlaces
        expected_url = SERVER_URL + "/purchasePlaces"
        current_url = driver.current_url
        assert expected_url in current_url
        time.sleep(2)

    # logout
    logout_link = driver.find_element(By.CLASS_NAME, "logout")
    logout_link.click()
    expected_url = SERVER_URL
    current_url = driver.current_url
    assert expected_url in current_url
    time.sleep(2)


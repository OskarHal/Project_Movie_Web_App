import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium


class MovieBuffTests(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome('chromedriver.exe')

    def test_search(self):
        self.driver.get('http://127.0.0.1:5000')

        search_field = self.driver.find_element_by_id('search')
        search_field.clear()
        search_field.send_keys('Inception')
        search_field.send_keys(Keys.RETURN)
        search_results = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'result')))
        results = search_results.find_elements_by_name("movie-box")

        for result in results:
            self.assertIn('Inception', result.text)
        self.assertEqual(len(results), 10)

    def test_signup(self):
        self.driver.get('http://127.0.0.1:5000/signup')

        first_name_field = self.driver.find_element_by_id('first-name')
        last_name_field = self.driver.find_element_by_id('last-name')
        email_field = self.driver.find_element_by_id('email')
        username_field = self.driver.find_element_by_id('username')
        password_field = self.driver.find_element_by_id('password')
        confirm_field = self.driver.find_element_by_id('confirm')
        submit = self.driver.find_element_by_id('submit')

        first_name_field.send_keys('Test')
        last_name_field.send_keys('Testsson')
        email_field.send_keys('test@test.se')
        username_field.send_keys('test123')
        password_field.send_keys('test123')
        confirm_field.send_keys('test123')
        submit.send_keys(Keys.RETURN)

        expectedUrl = "http://127.0.0.1:5000/"
        actualUrl = self.driver.current_url
        self.assertEquals(expectedUrl, actualUrl)

    def test_login(self):
        self.driver.get('http://127.0.0.1:5000')

        email_field = self.driver.find_element_by_id('email')
        password_field = self.driver.find_element_by_id('password')
        submit = self.driver.find_element_by_name('submit')

        email_field.send_keys('test@test.se')
        password_field.send_keys('test123')
        submit.send_keys(Keys.RETURN)

        expectedUrl = "http://127.0.0.1:5000/profile"
        actualUrl = self.driver.current_url
        self.assertEqual(actualUrl, expectedUrl)

    def test_add_friend(self):
        self.test_login()

        self.driver.get('http://127.0.0.1:5000/friends')
        username_field = self.driver.find_element_by_id('add')
        submit = self.driver.find_element_by_id('add-submit')

        num_friends_before = len(self.driver.find_elements_by_class_name('friend-link'))
        username_field.send_keys('hanna')
        submit.send_keys(Keys.RETURN)
        num_friends_after = len(self.driver.find_elements_by_class_name('friend-link'))
        print(num_friends_before)
        print(num_friends_after)

    def test_send_message(self):
        self.test_login()

        self.driver.get('http://127.0.0.1:5000/friends')

        friends = self.driver.find_elements_by_class_name('friend-link')
        friend_link = friends[0]
        friend_link.click()

        # text_input = self.driver.find_element_by_id('send')
        text_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'send')))
        submit = self.driver.find_element_by_id('send_submit')

        # Funkar ej

        text_input.click()
        # time.sleep(1)
        text_input.send_keys('hur är läget?!')
        submit.send_keys(Keys.RETURN)
        print(text_input.get_attribute('value').encode('utf-8'))
        print(self.driver.page_source)
        time.sleep(5)

    def test_add_to_watchlist(self):
        self.test_login()
        self.test_search()

        WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.NAME, 'movie-box')))[0].click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'add'))).click()

        self.driver.get('http://127.0.0.1:5000/watchlist')

        movie_title = self.driver.find_element_by_id('main-container').text
        self.assertEqual(movie_title, "Inception")

    def test_add_profile_picture(self):
        self.test_login()
        self.driver.get('http://127.0.0.1:5000/profile')
        submit_button = self.driver.find_element_by_id('file')

        self.driver.close()

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()

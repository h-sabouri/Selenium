from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import string
import random
import time


class InvalidUserLoginError:
    url = 'http://demostore.supersqa.com/my-account/'
    invalid_email = 'abcde@supersqa.com'
    expected_message = 'Unknown email address. Check again or try your username.'
    coupon_code = "SSQA100"

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        time.sleep(2)
        self.letters = string.ascii_letters
        self.random_string = ''.join(random.choice(self.letters) for i in range(15))
        self.random_email = self.random_string + "@supersqa.com"
        self.random_letters = string.ascii_letters
        random_string = ''.join(random.choice(self.letters) for j in range(6))
        self.random_pass = random_string + '@' + 'len(random_string)'
        self.wait = WebDriverWait(self.driver, 10)

    def go_to_my_account(self):
        self.driver.get(self.url)

    def input_email(self):
        email_field = self.driver.find_element(By.ID, 'reg_email')
        email_field.send_keys(self.random_email)

    def input_reg_pass(self):
        pass_field = self.driver.find_element(By.ID, 'reg_password')
        pass_field.send_keys(self.random_pass)

    def click_register(self):
        register_btn = self.driver.find_element(By.CSS_SELECTOR, '.woocommerce-Button')
        register_btn.click()

    def verify_message(self):

        logout_btn = self.driver.find_element(By.CSS_SELECTOR,
                                              'li.woocommerce-MyAccount-navigation-link:nth-child(6) > a:nth-child(1)')

        if logout_btn.is_displayed():
            print("pass!")
        else:
            raise Exception("User didn't logged in after registering")
        logout_btn.click()

    def input_username(self):
        email_field = self.driver.find_element(By.ID, 'username')
        email_field.send_keys(self.invalid_email)

    def input_password(self):
        pass_field = self.driver.find_element(By.ID, 'password')
        pass_field.send_keys('absjdasd')

    def click_login(self):
        login_field = self.driver.find_element(By.NAME, 'login')
        login_field.click()

    def verify_error_message(self):
        err_element = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/div/div[1]/ul/li')
        displayed_message_err = err_element.text
        assert displayed_message_err == self.expected_message;
        "The Displayed error is not expected"
        print('pass')

    def home_btn(self):
        home_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div/nav/a')
        home_btn.click()

    def add_1_item_to_cart(self):
        add_item_1 = self.driver.find_element(By.CLASS_NAME, 'add_to_cart_button')
        add_item_1.click()
        self.wait.until(
            EC.text_to_be_present_in_element((By.XPATH, '/html/body/div[2]/header/div[2]/div/ul/li[1]/a/span[2]'),
                                             '1 item')
        )

    def click_cart_in_top(self):
        cart_btn = self.driver.find_element(By.XPATH, '/html/body/div[2]/header/div[2]/div/ul/li[1]/a')
        cart_btn.click()

    def input_coupon_and_hit_enter(self, coupon_code):
        coupon_field = self.wait.until(EC.visibility_of_element_located((By.ID, 'coupon_code')))
        coupon_field.send_keys(coupon_code)
        coupon_field.send_keys(Keys.ENTER)

    def verify_total_is_0(self):
        # We need to wait in order to the value of the Total to be changed:
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH,
                                                          '/html/body/div[2]/div[2]/div/div['
                                                          '2]/main/article/div/div/div[2]/div/table/tbody/tr['
                                                          '4]/td/strong/span/bdi'),
                                                         '$0.00'))

    def main(self):
        self.go_to_my_account()
        self.input_username()
        time.sleep(2)
        self.input_password()
        time.sleep(2)
        self.click_login()
        self.verify_error_message()
        time.sleep(2)
        self.input_email()
        time.sleep(2)
        self.input_reg_pass()
        time.sleep(2)
        self.click_register()
        # self.verify_message()
        time.sleep(2)
        self.home_btn()
        time.sleep(2)
        self.add_1_item_to_cart()
        time.sleep(2)
        self.click_cart_in_top()
        time.sleep(2)
        self.input_coupon_and_hit_enter(self.coupon_code)
        time.sleep(2)
        self.verify_total_is_0()

        # self.driver.quit()


"""
when we have if name == 'main' we're telling it whenever we run script directly to execute that part.
But, when we import the script into another script, do not execute that
"""

if __name__ == '__main__':
    obj = InvalidUserLoginError()
    obj.main()

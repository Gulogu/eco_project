import logging

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

class CheckOutPage:
    CART_TOTAL = (By.ID, 'cart-total')
    CHECKOUT_BTN = (By.XPATH, '//p[@class="text-right"]/a[2]')
    GUEST_ACCOUNT_RADIO = (By.XPATH, '//input[@value="guest"]')
    CONTINUE_ACCOUNT_BTN = (By.XPATH, '//input[@id="button-account"]')
    ACCORDION_TOGGLE = (By.CSS_SELECTOR, '.accordion-toggle')
    INPUT_FIRSTNAME = (By.ID, 'input-payment-firstname')
    INPUT_LASTNAME = (By.ID, 'input-payment-lastname')
    INPUT_EMAIL = (By.ID, 'input-payment-email')
    INPUT_TELEPHONE = (By.ID, 'input-payment-telephone')
    INPUT_ADDRESS = (By.ID, 'input-payment-address-1')
    INPUT_CITY = (By.ID, 'input-payment-city')
    INPUT_POSTCODE = (By.ID, 'input-payment-postcode')
    DROPDOWN_COUNTRY = (By.ID, 'input-payment-country')
    # DROPDOWN_REGION = (By.ID, 'input-payment-zone')
    CONTINUE_GUEST_BTN = (By.ID, 'button-guest')
    CONTINUE_SHIPPING_BTN = (By.ID, 'button-shipping-method')
    AGREE_TERMS_CHECKBOX = (By.XPATH, '//input[@name="agree"]')
    CONTINUE_PAYMENT_BTN = (By.ID, 'button-payment-method')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def click_element(self,locator:tuple):
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            logging.info(f"点击元素成功: {locator}")
        except TimeoutException:
            logging.error(f"元素不可点击: {locator}")
            self.driver.save_screenshot("click_element_failure.png")
            raise

    def input_text(self, locator, text: str):
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            element.clear()
            element.send_keys(text)
            logging.info(f"输入文本成功: {locator}")
        except TimeoutException:
            logging.error(f"元素不可输入: {locator}")
            self.driver.save_screenshot("input_text_failure.png")
            raise

    def select_dropdown(self, dropdown_locator, option_text: str):
        try:

            dropdown = self.wait.until(EC.element_to_be_clickable(dropdown_locator))
            Select(dropdown).select_by_visible_text(option_text)
            logging.info(f"选择下拉成功: {dropdown_locator}")
        except TimeoutException:
            logging.error(f"选择下拉失败: {dropdown_locator}")
            self.driver.save_screenshot("select_dropdown_failure.png")
            raise
    def go_to_checkout(self):
        logging.info("===前往结账页面===")
        self.click_element(self.CART_TOTAL)
        self.click_element(self.CHECKOUT_BTN)
        logging.info("成功进入结账页面")

    def select_guest_account(self):
        logging.info("选择访客账户")
        self.click_element(self.GUEST_ACCOUNT_RADIO)
        self.click_element(self.CONTINUE_ACCOUNT_BTN)
        logging.info("选择访客账户成功")

    def fill_shipping_info(self,first_name,last_name,email,telephone,address,city,postcode,country):
        logging.info("开始填写信息")
        # self.click_element(self.ACCORDION_TOGGLE)
        self.input_text(self.INPUT_FIRSTNAME,first_name)
        self.input_text(self.INPUT_LASTNAME,last_name)
        self.input_text(self.INPUT_EMAIL,email)
        self.input_text(self.INPUT_TELEPHONE,telephone)
        self.input_text(self.INPUT_ADDRESS,address)
        self.input_text(self.INPUT_CITY,city)
        self.input_text(self.INPUT_POSTCODE,postcode)
        self.select_dropdown(self.DROPDOWN_COUNTRY,country)
        # self.select_dropdown(self.DROPDOWN_REGION,region)
        logging.info("信息填写成功")

    def submit_checkout_steps(self):
        logging.info("开始结账步骤")
        self.click_element(self.CONTINUE_GUEST_BTN)
        self.click_element(self.CONTINUE_SHIPPING_BTN)
        self.click_element(self.AGREE_TERMS_CHECKBOX)
        self.click_element(self.CONTINUE_PAYMENT_BTN)
        logging.info("结账完成")





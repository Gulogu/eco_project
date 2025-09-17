import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import logging
import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.iphonePage import navigate_thumbnails
from pages.laptoppage import hover_and_click
from pages.HPpage import hp_click
from pages.CheckOutpage import CheckOutPage
from selenium.webdriver.support.select import Select
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



# 初始化WebDriver
@allure.title("完整购物流程测试")
def test_shopping_flow():
    logging.info("开始执行测试用例")


#访问网站
driver_path = r"F:\code\webdrivers\chrome\chromedriver.exe"  #指定chromedriver路径
service = Service(executable_path=driver_path)  #创建servive对象
driver = webdriver.Chrome(service=service)  #创建webdrive，传入service参数
driver.get("https://tutorialsninja.com/demo/")
driver.maximize_window()
logging.info("访问网站成功")

wait = WebDriverWait(driver, 10)
#选择手机分类
with allure.step("选择手机分类"):
    phone = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[text()="Phones & PDAs"]'))
    )
    phone.click()

with allure.step("验证iphone商品详情页"):
    iphone = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[text()="iPhone"]')))
try:
    iphone.click()
except Exception as e:
    logging.error(f"进入iphone详情页失败: {str(e)}")

#验证页面跳转
wait.until(
    EC.url_contains("product_id=40")
)
logging.info("成功进入iphone详情页")

with allure.step("截图"):
    try:

        navigate_thumbnails(driver,5, 10)

        timestamp = time.strftime("%Y%m%d-%H%M%S")
        screenshot_name = f"screenshot_{timestamp}.png"
        driver.save_screenshot(screenshot_name)
        logging.info(f"保存截图：{screenshot_name}")

        close = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@title="Close (Esc)"]')))
        close.click()
        logging.info("关闭成功")
        # add_to_button = driver.find_element(By.ID,'button-cart')
        # add_to_button.click()
        # time.sleep(2)

    except Exception as e:
        logging.critical(f"测试流程中断: {str(e)}")
        driver.save_screenshot("critical_failure.png")
        raise


with allure.step("购买laptop"):
    try:
        hover_and_click(driver,target_text="Laptops & Notebooks",sub_target_text="Show AllLaptops & Notebooks")
        hp_click(driver, target_xpath="//a[text()='HP LP3065']", action_element_xpath="#button-cart")

        # calendar
        calendar = driver.find_element(By.XPATH,'//i[@class="fa fa-calendar"]')
        calendar.click()
        time.sleep(2)


        next_click_calandar = driver.find_element(By.XPATH,'//th[@class="next"]')
        month_year = driver.find_element(By.XPATH,'//th[@class="picker-switch"]')

        #year:2022  month:december
        while month_year.text != 'December 2022':
            next_click_calandar.click()
            time.sleep(0.1)

        #day:31
        calandar_day = driver.find_element(By.XPATH,'//td[text()="31"]')
        calandar_day.click()
        time.sleep(2)




    except Exception as e:
        logging.critical(f"测试流程中断: {str(e)}")
        raise

with allure.step("结账流程"):
    checkout_page = CheckOutPage(driver)
    try:
            checkout_page.go_to_checkout()
            checkout_page.select_guest_account()
            checkout_page.fill_shipping_info(
            first_name="test_first_name",
            last_name="test_last_name",
            email="test@test.com",
            telephone="44444555555",
            address="street",
            city="test city",
            postcode="11222",
            country="Germany",
            )
            region = driver.find_element(By.ID, 'input-payment-zone')
            dropdown_2 = Select(region)
            dropdown_2.select_by_index(1)
            checkout_page.submit_checkout_steps()
    except Exception as e:
            logging.critical(f"测试失败: {str(e)}", exc_info=True)
            driver.save_screenshot("checkout_flow_failure.png")
            raise

    # 最终价格验证
with allure.step("验证最终价格"):
        final_price_element = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//table[@class = "table table-bordered table-hover"]/tfoot/tr[3]/td[2]'))
        )
        final_price = final_price_element.text
        assert final_price != "", "价格未正确显示"
        logging.info(f"最终价格: {final_price}")

    # 订单成功验证
with allure.step("验证订单"):
        success_title = wait.until(
            EC.visibility_of_element_located((By.ID,'button-confirm'))
        )
        success_title.click()
        assert success_title.is_displayed(), "订单成功页面未正确显示"
        logging.info("订单创建成功")
        success_text = driver.find_element(By.XPATH, '//div[@class = "col-sm-12"]/h1')
        logging.info(f"订单成功文本：{success_text.text}")



if __name__ == "__main__":
    pytest.main(["-s", "--alluredir", "./reports"])











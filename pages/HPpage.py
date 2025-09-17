import logging

from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def select_calendar(driver,year,month,day):
    try:
        calendar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,'//i[@class="fa fa-calendar"]'))
        )
        calendar.click()
        logging.info("点击成功")
        while True:
            current_month_year = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH,'//th[@class="picker-switch"]'))
            ).text
            if current_month_year == f"{month} {year}":
                break
            next_click_calandar = driver.find_element(By.XPATH,'//th[@class="next"]')
            next_click_calandar.click()
            logging.info("点击下个月按钮")

            day = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,f"//td[text()='{day}']"))
            )
            day.click()
            logging.info(f"选择日期'{year}/{month}/{day}'成功")
    except Exception as e:
        logging.error(f"日历选择失败：str{e}")
        driver.sava_screenshot("calendar_select_failure.png")
        raise

def hp_click(driver,target_xpath,action_element_xpath):
    try:
        hp = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,target_xpath))
        )
        ActionChains(driver).move_to_element(hp).perform()
        logging.info(f"悬停到'{target_xpath}'成功")
        hp.click()
        if action_element_xpath:
            action_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,action_element_xpath))
            )
            action_element.click()
            logging.info(f"点击'{action_element_xpath}'成功")
    except Exception as e:
        logging.error(f"操作失败: str{e}")
        driver.save_screenshot("HP_click_failure.png")
        raise






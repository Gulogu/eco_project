import logging

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def hover_and_click(driver,target_text,sub_target_text):
    try:
        laptops = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,f'//a[text()="{target_text}"]')))
        ActionChains(driver).move_to_element(laptops).perform()
        logging.info(f"悬停到{target_text}成功")

        laptops_2 = WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.XPATH,f'//a[text()="{sub_target_text}"]'))
        )
        laptops_2.click()
        logging.info(f"点击 '{sub_target_text}' 成功")
    except Exception as e:
        logging.error(f"操作失败: {str(e)}")
        driver.save_screenshot("hover_click_failure.png")
        raise





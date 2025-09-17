import logging
import time

from selenium.webdriver.common.by import By




# 定义图片轮播操作封装函数
def navigate_thumbnails(driver, num_slides = 5, wait_time = 10):
    try:
        # 点击第一张
        # first_page = WebDriverWait(driver,wait_time).until(
        #     EC.element_to_be_clickable((By.XPATH, '//ul[@class="thumbnails"]/li[1]'))
        # )
        # first_page.click()
        # logging.info("点击第一张图片成功")
        first_page = driver.find_element(By.CSS_SELECTOR, 'ul.thumbnails li:first-child')
        first_page.click()
        time.sleep(2)
        # #切换
        # next_page = WebDriverWait(driver,wait_time).until(
        #     EC.element_to_be_clickable((By.XPATH, '//button[@title="Next (Right arrow key)"]'))
        # )
        # for _ in range(num_slides):
        #     next_page.click()
        #     WebDriverWait(driver, wait_time).until(
        #         EC.staleness_of(first_page)  # 等待图片更新
        #     )
        #     logging.info(f"✅ 切换到下一张图片（共{_ + 1}/{num_slides}）")

        next_page = driver.find_element(By.CSS_SELECTOR, 'button[title="Next (Right arrow key)"]')
        for i in range(0, 5):
            next_page.click()
            time.sleep(2)
            logging.info(f"切换到下一张图片，共{i + 1}/{num_slides}")

    except Exception as e:
        logging.error(f"切换失败", {str(e)})
        driver.save_screenshot("thumbnail_navigation_failure.png")
        raise









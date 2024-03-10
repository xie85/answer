import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

def fetch_exchange_rate(date, currency_code, driver_path):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 无头模式
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://www.boc.cn/sourcedb/whpj/")
        
        # 输入日期，这里假设你只需要输入起始日期
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "erectDate"))
        ).send_keys(date)

        # 选择货币
        select = Select(WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "pjname"))
        ))
        # 根据提供的货币代号选择正确的选项
        if currency_code == "USD":
            select.select_by_visible_text("美元")
        elif currency_code == "EUR":
            select.select_by_visible_text("欧元")
        # 为其他货币代号添加相应的elif语句

        # 点击搜索按钮
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@class='search_btn']"))
        )
        search_button.click()

        # 等待结果加载
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='BOC_main publish']"))
        )

        # 提取现汇卖出价
        # 注意：此处XPath可能需要根据实际页面结构调整
        rate = driver.find_element(By.XPATH, "//table[@class='BOC_main publish']/tbody/tr[2]/td[4]").text
        return rate
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python yourcode.py <YYYYMMDD> <CurrencyCode> <PathToChromeDriver>")
        sys.exit(1)

    date, currency_code, driver_path = sys.argv[1], sys.argv[2], sys.argv[3]
    exchange_rate = fetch_exchange_rate(date, currency_code, driver_path)

    if exchange_rate:
        print(f"Exchange Rate: {exchange_rate}")
        # Write the exchange rate to result.txt
        with open("result.txt", "w") as file:
            file.write(f"Date: {date}, Currency: {currency_code}, Exchange Sell Rate: {exchange_rate}")
    else:
        print("Failed to fetch the exchange rate.")

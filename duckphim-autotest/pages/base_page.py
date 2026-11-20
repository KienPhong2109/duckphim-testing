from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.settings import BASE_URL, TIMEOUT
from utils.logger import step


class BasePage:
    """Lớp cha: chứa các thao tác mà trang nào cũng cần (mở trang, tìm, bấm, gõ)."""

    def __init__(self, driver):
        self.driver = driver
        
        self.wait = WebDriverWait(driver, TIMEOUT)

    def open(self, path):
        step(f"Mở trang: {BASE_URL}/{path}")
        self.driver.get(f"{BASE_URL}/{path}")

    
    def find(self, locator):
        step(f"Tìm phần tử {locator}")
        return self.wait.until(EC.visibility_of_element_located(locator))

    
    def find_all(self, locator):
        step(f"Tìm danh sách phần tử {locator}")
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        step(f"Bấm vào {locator}")

        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', behavior: 'instant'});", element
        )
        
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text, secret=False):
        shown = "******" if secret else text
        step(f"Gõ '{shown}' vào {locator}")
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    @property
    def title(self):
        return self.driver.title
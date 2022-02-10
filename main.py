import json
from typing import Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


class Bot:
    def __init__(self):
        """
        Bot class
        """
        self.driver = webdriver.Chrome()

    @staticmethod
    def load_credentials() -> Tuple[str, str]:
        """
        Load user's credentials stored in credentials.json as {"email": "exemple@email.fr", "password": "SigmaPassword"}
        :return: email, password
        """
        with open("credentials.json", "r") as file:
            credentials = json.loads(file.read())
        return credentials['email'], credentials['password']

    def login(self, email, password):
        """
        Login to global exam
        :param email: user's email
        :param password: user's password
        """
        input_email: WebElement = WebDriverWait(self.driver, timeout=2000).until(
            lambda d: d.find_element(By.ID, "email"))
        input_email.click()
        action = ActionChains(self.driver)
        action.send_keys(email)
        action.perform()

        input_password: WebElement = self.driver.find_element(By.ID, "password")
        input_password.click()
        action = ActionChains(self.driver)
        action.send_keys(password)
        action.perform()

    def run(self):
        """
        Run the bot
        """
        self.driver.get("https://auth.global-exam.com/login")

        email, password = self.load_credentials()
        self.login(email, password)
        input()

        self.driver.quit()


if __name__ == "__main__":
    bot = Bot()
    bot.run()

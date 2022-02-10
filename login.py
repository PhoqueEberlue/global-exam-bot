import yaml
settings = yaml.safe_load(open("./settings.yaml"))['settings']

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


def login(driver):
    assert "email" in settings or "password" in settings, print("No email / password !")

    driver.implicitly_wait(10)
    if not driver.current_url == "https://auth.global-exam.com/login":
        return print("already logged")

    emailLogin = driver.find_element(By.NAME, "email")
    passwordLogin = driver.find_element(By.NAME, "password")

    emailLogin.send_keys(settings["email"])
    passwordLogin.send_keys(settings["password"])
    driver.find_element_by_class_name("button-solid-primary-big mb-6")

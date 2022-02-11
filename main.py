import time
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
        self.questionTimeInterval = 5 #NOTE change to 60s+ for release

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
        # Checks if not already logged
        if not self.driver.current_url == "https://auth.global-exam.com/login":
            print("already logged")

        # Gets email input element when the webpage is ready
        input_email: WebElement = WebDriverWait(self.driver, timeout=2000).until(
            lambda d: d.find_element(By.ID, "email"))
        input_email.click()
        action = ActionChains(self.driver)
        # Fill input
        action.send_keys(email)
        action.perform()

        # Gets password input element
        input_password: WebElement = self.driver.find_element(By.ID, "password")
        input_password.click()
        action = ActionChains(self.driver)
        # Fill input
        action.send_keys(password)
        action.perform()

        # Gets the login button
        log_button: WebElement = self.driver.find_element(By.CSS_SELECTOR, "#login-form > div.text-center > button")
        log_button.click()
        

    def isSessionFinished(self): #TODO session timer
        return False

    def doPhraseATrou(self, ex):
        ex.click()

        start: WebElement = WebDriverWait(self.driver, timeout=2000).until(
            lambda d: d.find_element(By.XPATH,\
                "//*[ contains (text(), 'arrer' )]" ))
        if start: start.click()

        showCorrection: WebElement = WebDriverWait(self.driver, timeout=2000).until(
            lambda d: d.find_elements(By.XPATH,\
                    "//*[ contains (text(), 'Voir' )]")) #YOINK

        for bttn in showCorrection:
            bttn.click()

        solution = self.driver.find_elements(By.CSS_SELECTOR, \
                "text-success-80 svg-inline--fa fa-check fa-w-16 fa-fw fa-lg")
                #NOTE should do xpath + tag, this doesnt work
        for bttn in solution:
            time.sleep(self.questionTimeInterval) #maybe not necessary, ugly,
            bttn.click()
        # hide ? 
        for bttn in showCorrection:
            bttn.click()                        # but does exactly what we want

        self.driver.find_elements_by_class_name(\
                'min-w-48 button-solid-primary-large')
        #yay
        print("should have worked")




    def launch_phrase_a_trou(self): #only launcher or doPhraseATrou ?
         # i tried something, remove if ugly
        self.driver.get(\
            "https://exam.global-exam.com/library/trainings/exercises/492/activities")

        exListe = self.getDoableEx()

        while not self.isSessionFinished() and exListe: #latter one checks vacuity
            ex = exListe.pop() #possible in one line ?
            self.doPhraseATrou(ex)
        # TODO time session, stop after X sec
        # NOTE ik how to do that, remind me if i forget

    def getDoableEx(self):
        return WebDriverWait(self.driver, timeout=2000).until(
            lambda d: d.find_elements(By.XPATH,\
                    "//*[ contains (text(), 'Lancer' )]")) #YOINK

    def run(self):
        """
        Run the bot
        """
        self.driver.get("https://auth.global-exam.com/login")

        email, password = self.load_credentials()

        self.login(email, password)

        self.launch_phrase_a_trou() #TODO choice if we got time
        print('fuck')
        input() #wat


if __name__ == "__main__":
    bot = Bot()
    bot.run()

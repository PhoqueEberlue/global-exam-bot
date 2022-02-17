import time
import json
from typing import Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException as StaleElt


class Bot:
    def __init__(self):
        """
        Bot class
        """
        self.driver = webdriver.Chrome()
        self.actions = ActionChains(self.driver)
        self.questionTimeInterval = 4 #NOTE change to 60s+ for release
        self.timeStart = int(time.time())
        self.sessionTime = 10*60

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
        input_email: WebElement = WebDriverWait(self.driver, timeout=2).until(
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
        return int(time.time() - self.timeStart) > self.sessionTime

    def finishing(self):
        return print("finished")



    def doPhraseATrou(self):
        shouldContinue = True
        while shouldContinue:
            if "result" in self.driver.current_url: return self.finishing()
            showCorrection = []

            try: 
                showCorrection = WebDriverWait(self.driver, timeout=5).until(
                lambda d: d.find_elements(By.XPATH,\
                        "//*[ contains (text(), 'Voir' )]"))
            except TimeoutException:
                shouldContinue = False; print("\033[0;39;49m;[no"); return

            for bttn in showCorrection:
                self.actions.move_to_element(bttn).perform()
                bttn.click()

            solution = self.driver.find_elements(By.XPATH,\
                    "//*[contains (@class, 'text-success-80 svg-inline--fa fa-check fa-w-16 fa-fw fa-lg')]")

            ##gotta request again maybe idk seems to work ?
            #showCorrection: WebElement = WebDriverWait(self.driver, timeout=2).until(
            #    lambda d: d.find_elements(By.XPATH,\
            #            "//*[contains (text(), 'Voir')]"))

            for bttn in solution:
                self.actions.move_to_element(bttn).perform()
                time.sleep(self.questionTimeInterval)
                bttn.click()


            for bttn in showCorrection:#hide
                self.actions.move_to_element(bttn).perform()
                bttn.click()

            self.driver.find_element(By.XPATH,\
                    '//*[contains (@class, "min-w-48 button-solid-primary-large")]').click()
            #yay
        print("should have worked")


    def beginExercie(self):
        start: WebElement 
        try:
            start = WebDriverWait(self.driver, timeout=2).until(
            lambda d: d.find_element(By.CLASS_NAME,\
                "button-solid-primary-medium" ))
            start.click()
        except TimeoutException:
            print("no start page")

        return self.doPhraseATrou()

    def launch_phrase_a_trou(self): #only launcher or doPhraseATrou ?
         # i tried something, remove if ugly
        self.driver.get(\
            "https://exam.global-exam.com/library/trainings/exercises/492/activities")

        exListe = self.getDoableEx()

        while not self.isSessionFinished() and exListe: #later one checks vacuity
            ex = exListe.pop() #possible in one line ?
            try: 
                ex.click()
            except StaleElt:
                print("HERE 140")
                
            time.sleep(4)
            self.beginExercie()
        print("finished ! :)")

    def getDoableEx(self):
        return WebDriverWait(self.driver, timeout=2000).until(
            lambda d: d.find_elements(By.XPATH,\
                    "//*[ contains (text(), 'Lancer') or contains (text(), 'Continuer')]")) #YOINK gotta redo later

    def run(self):
        """
        Run the bot
        """
        self.driver.get("https://auth.global-exam.com/login")

        email, password = self.load_credentials()

        self.login(email, password)

        self.launch_phrase_a_trou() #TODO choice if we got time


if __name__ == "__main__":
    bot = Bot()
    bot.run()

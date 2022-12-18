from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import re

def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'', text)


class Bot:
    def __init__(self):
        self.driver = webdriver.Firefox()

    def visit(self, bot_type: str, language='en'):

        # Visit the website
        self.driver.get('https://www.{}.com/{}/'.format(bot_type.lower(), language.lower()))

        # Click undrestood button
        # For some reason an iframe blocks the button from being able to click so I just executed the onclick script.
        # Also, switching to the iframe didn't work
        understoodButton = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'understood')))
        onClickScript = understoodButton.get_attribute('onclick')
        self.driver.execute_script(onClickScript)

        # Find input bar
        self.inputBar = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'stimulus')))


    # Say something to bot
    def say(self, message: str):
        message = deEmojify(message)
        self.inputBar.send_keys(message)
        self.inputBar.send_keys(Keys.ENTER)

    # Get last message of bot
    def getLastMessage(self):

        while self.driver.find_element(By.ID, 'line1').find_element(By.CLASS_NAME, 'bot').text == ' ':
            pass
        previous = self.driver.find_element(By.ID, 'line1').find_element(By.CLASS_NAME, 'bot').text
        while True:
            sleep(0.5)
            if self.driver.find_element(By.ID, 'line1').find_element(By.CLASS_NAME, 'bot').text == previous:
                break
            previous = self.driver.find_element(By.ID, 'line1').find_element(By.CLASS_NAME, 'bot').text
        return previous

    def close(self):
        self.driver.close()


def main():

    # You can change it to whatever bot you want
    firstBot = Bot()
    firstBot.visit(bot_type='eviebot')

    secondBot = Bot()
    secondBot.visit(bot_type='boibot')

    while True:
        firstBot.say(secondBot.getLastMessage())
        secondBot.say(firstBot.getLastMessage())

if __name__ == '__main__':
    main()

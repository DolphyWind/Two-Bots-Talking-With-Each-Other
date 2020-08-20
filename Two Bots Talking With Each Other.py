from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import re

def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)


class Bot:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def visit(self, bot_type: str, language='en'):

        # Visit the website
        self.driver.get('https://www.{}.com/{}/'.format(bot_type.lower(), language.lower()))

        # Find input bar
        while True:
            try:
                self.inputBar = self.driver.find_element_by_class_name('stimulus')
            except: pass
            else: break

    # Say something to bot
    def say(self, message: str):
        message = deEmojify(message)
        self.inputBar.send_keys(message)
        self.inputBar.send_keys(Keys.ENTER)

    # Get last message of bot
    def getLastMessage(self):
        while self.driver.find_element_by_id('line1').find_element_by_class_name('bot').text == ' ':
            pass
        previous = self.driver.find_element_by_id('line1').find_element_by_class_name('bot').text
        while True:
            sleep(0.5)
            if self.driver.find_element_by_id('line1').find_element_by_class_name('bot').text == previous:
                break
            previous = self.driver.find_element_by_id('line1').find_element_by_class_name('bot').text
        return previous

    def close(self):
        self.driver.close()


def main():

    # You can change it to whatever bot you want
    evie = Bot()
    evie.visit(bot_type='eviebot')

    pewdie = Bot()
    pewdie.visit(bot_type='pewdiebot')

    while True:
        evie.say(pewdie.getLastMessage())
        pewdie.say(evie.getLastMessage())

if __name__ == '__main__':
    main()

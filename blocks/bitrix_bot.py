#selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
#selenium
from time import sleep

def Prt(arg):
    driver = webdriver.Chrome('/home/sgpro1991/app/plan/driver/chromedriver')
    driver.get("https://oblgazeta.bitrix24.ru/")
    driver.find_element_by_name('USER_LOGIN').send_keys('sgpro@oblgazeta.ru')
    driver.find_element_by_name('USER_PASSWORD').send_keys('i6C7Cq')
    driver.find_element_by_id("AUTH_SUBMIT").click()
    driver.find_element(By.XPATH, '//*[@id="microoPostFormLHE_blogPostForm"]/span[1]').click();
    driver.find_element(By.XPATH, '//*[@id="bx-html-editor-iframe-cnt-idPostFormLHE_blogPostForm"]/iframe').send_keys(arg);

    sleep(50)


    #while True:
    #    pass

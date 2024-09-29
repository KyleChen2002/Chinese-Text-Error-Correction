from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

#coding = utf-8
name = []
password = []
result = []
#读取纠错文件
f = open('text.txt','r',encoding='UTF-8',errors = 'ignore')
text = f.readlines()
f.close()
#读取用户信息
f_users = open('users.txt','r',encoding='UTF-8',errors = 'ignore')
lines = f_users.readlines()      #读取全部内容 ，并以列表方式返回
for line in lines:
    x = line.split()
    name.append(x[0])
    password.append(x[1])
print(name)
print(password)
user_num = len(name)
f_users.close()

driver = webdriver.Firefox()
driver.get('http://127.0.0.1:5001/login.html')
driver.find_element(By.ID,'username').send_keys('cjk')
driver.find_element(By.ID,'password').send_keys('654321')
driver.find_element(By.XPATH,'/html/body/section/form/input[3]').click()
if(driver.title == '纠错demo pycorrector-ai.jry'):
    print('right')
    driver.find_element(By.ID,'input_text').send_keys(text)
    sleep(3)
    driver.find_element(By.XPATH,'/html/body/section/div/div[1]/form/input').click()
    url_right = 'http://127.0.0.1:5001/do_check'
    if(driver.current_url == url_right):
        print('text right')
        sleep(3)
        driver.find_element(By.XPATH,'/html/body/nav/ul/li[2]/a').click()

sleep(10)
driver.quit()
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
import tkinter as tk
from tkinter.messagebox import *
import csv

root = tk.Tk()  # 创建主窗口
root.title('AUTO-SIGH')  # 命名
root.geometry('500x500+200+100')  # 调整大小
root.resizable(0, 0)  # 不允许改变大小
root.attributes('-alpha', 0.9)
root['background'] = '#ffffff'


L_name = tk.Label(root, text='学号')
L_name.place(relx=0.3, rely=0.3, anchor="center")
E_name = tk.Entry(root, bd=5)
E_name.place(relx=0.5, rely=0.3, anchor="center")


L_password = tk.Label(root, text = '密码')
L_password.place(relx=0.3, rely=0.35, anchor="center")
E_password = tk.Entry(root, bd=5, show='*')
E_password.place(relx=0.5, rely=0.35, anchor="center")

START = tk.Button(root, text='自动打卡', font=('宋体', 16, 'bold'),
                      relief=tk.FLAT, bg='#98FB98')
START.place(relx=0.5, rely=0.5, anchor="center")

def auto_sign():
    USERNAME = str(E_name.get())
    PASSWORD = str(E_password.get())
    options = webdriver.ChromeOptions()
    prefs = {
    'profile.default_content_setting_values' :
    {
    'notifications' : 2
     }
    }
    options.add_experimental_option('prefs',prefs)


    try:
        web_driver = webdriver.Chrome(options=options)
    except:
        result = showinfo('提示', '未安装ChromeDriver')
        print(f'提示：{result}')
        return
    web_driver.get('http://stu.sufe.edu.cn/stu/ncp/ncpIndex.jsp')
    sleep(2)

    def click_by_xpath(web, xpath):
        button = web.find_element(by=By.XPATH, value=xpath)
        button.click()

    username = '//*[@id="username"]/div/div[1]/div[1]/div/input'
    password = '//*[@id="username"]/div/div[2]/div[1]/div/input'

    username_input = web_driver.find_element(by=By.XPATH, value=username)
    password_input = web_driver.find_element(by=By.XPATH, value=password)

    username_input.clear()
    username_input.send_keys(USERNAME)
    password_input.clear()
    password_input.send_keys(PASSWORD)

    login = '//*[@id="username"]/div/button'
    click_by_xpath(web_driver, login)
    sleep(2)

    start = '/html/body/div[3]/div/a'
    try:
        click_by_xpath(web_driver, start)
    except:
        web_driver.quit()
        result = showinfo('提示', '账号或密码错误')
        print(f'提示：{result}')
        return

    sleep(1)
    #弹窗确认
    try:
        web_driver.switch_to.alert.accept()
    except:
        web_driver.quit()
        result = showinfo('提示', '今日已打卡')
        print(f'提示：{result}')
        return

    questions = [
    '//*[@id="form"]/div[2]/div[1]/div[6]/label[2]/div[1]',
    '//*[@id="form"]/div[2]/div[1]/div[8]/label[2]/div[1]',
    '//*[@id="form"]/div[2]/div[1]/div[10]/label[2]/div[1]',
    '//*[@id="form"]/div[2]/div[1]/div[14]/label[1]/div[1]',
    '//*[@id="form"]/div[2]/div[1]/div[19]/label[3]/div[1]',
    '//*[@id="form"]/div[2]/div[1]/div[21]/label[2]/div[1]',
    '//*[@id="form"]/div[2]/div[1]/div[24]/label[2]/div[1]',
    '//*[@id="form"]/div[2]/div[1]/div[26]/label[2]/div[1]',
    '//*[@id="form"]/div[2]/div[1]/div[29]/label[5]/div[1]',
    '//*[@id="form"]/div[2]/div[1]/div[32]/label[2]/div[1]',
    ]
    for question in questions:
        click_by_xpath(web_driver, question)

    submit = '//*[@id="submit"]'
    click_by_xpath(web_driver, submit)

    sleep(0.1)
    confirm_submit = '//*[@id="cofirmSubmit"]'
    try:
        click_by_xpath(web_driver, confirm_submit)
    except:
        web_driver.quit()
        result = showinfo('提示', '打卡失败')
        print(f'提示：{result}')
        return

    web_driver.quit()
    result = showinfo('提示', '打卡成功')
    print(f'提示：{result}')
    return

START.config(command=auto_sign)
root.mainloop()  # 处于显示状态
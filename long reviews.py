# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 13:00:48 2023

@author: James
"""

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import re
import xlrd
import pandas as pd
import numpy as np
import xlsxwriter


total = pd.DataFrame(columns = ["Username", "Date/time of review","Rating of film", "Useful","Useless","Content"])
driver = webdriver.Chrome()


def star(string):
    if string == None:
        return None
    if string == "力荐":
        return "5"
    elif string == "推荐":
        return "4"
    elif string == "还行":
        return "3"
    elif string == "较差":
        return "2"
    else:
        return "1"
    
    
def content_process(string):
    try:
        ls = string.split()
        # print(ls)
        useful , useless, index = useful_detect(ls)
        content = "".join(ls[: index])
        # if(type(useful) != int):
        #     print("content:",useful, useless)
        return (useful,useless,content)
    except:
        return (0,0,None)


def useful_detect(ls):
    for i in range(len(ls) - 1, -1, -1):
        try:
            useless = int(ls[i])
            useful = int(ls[i - 2])
            index = i -2
            return (useful, useless, index)
        except:
            pass
            

def scrape(URL, total):
    driver.get(URL) 
    try:
        fold = driver.find_element(By.LINK_TEXT, "有一些影评被折叠了")
        fold.click()
    except:
        pass
    
    time.sleep(5)
    expands = driver.find_elements(By.LINK_TEXT,"展开")
    for button in expands:
        button.click()
        time.sleep(10)
    s = requests.session()
    selenium_user_agent = driver.execute_script("return navigator.userAgent")
    s.headers.update({"user-agent": selenium_user_agent})
    
    for cookie in driver.get_cookies():
        s.cookies.set(cookie["name"], cookie["value"], domain= cookie["domain"])
        
    response = s.get(URL)
    soup = BeautifulSoup(response.content, "html.parser")
    
    comments = soup.find_all("div", "main review-item")
    rates = []
    for comment in comments:
        try:
            rates.append(comment.find("span",re.compile("allstar")).get("title"))
        except:
            rates.append(None)


    names = soup.find_all("a", "name")
    dates = soup.find_all("span","main-meta")
    contents = driver.find_elements(By.CLASS_NAME, "full-content")
    for i in range(len(names)):

        name = names[i]
        date = dates[i]
        (good, bad, content) = content_process(contents[i].text)
        row = {"Username": name, 
               "Date/time of review":date , 
               "Rating of film" : star(rates[i]), 
               "Useful" : good,
               "Useless" : bad,
               "Content": content}
        row = pd.DataFrame(row,index = [0])
        total = pd.concat([total,row], ignore_index = True)

        
    return total

URL = "https://movie.douban.com/subject/1291546/reviews?"
total = scrape(URL,total)

# index = 8200
# URL = f"https://movie.douban.com/subject/1291546/reviews?start={index}"
# while index < 8600:
#     URL = f"https://movie.douban.com/subject/1291546/reviews?start={index}"
#     print(index)
#     time.sleep(10)
#     total = scrape(URL, total)
#     index += 20
    
# print(total)
# with pd.ExcelWriter("Farewell My Concubine long reviews(8600).xlsx" , engine='xlsxwriter') as writer:
#     total.to_excel(writer, sheet_name = "Farewell My Concubine", index= False)

# total = pd.DataFrame(columns = ["Username", "Date/time of review","Rating of film", "Useful","Useless","Content"])
# index = 8600
# URL = f"https://movie.douban.com/subject/1291546/reviews?start={index}"
# while index < 9000:
#     URL = f"https://movie.douban.com/subject/1291546/reviews?start={index}"
#     print(index)
#     time.sleep(10)
#     total = scrape(URL, total)
#     index += 20
    
# print(total)
# with pd.ExcelWriter("Farewell My Concubine long reviews(9000).xlsx" , engine='xlsxwriter') as writer:
#     total.to_excel(writer, sheet_name = "Farewell My Concubine", index= False)
    
# total = pd.DataFrame(columns = ["Username", "Date/time of review","Rating of film", "Useful","Useless","Content"])
# index = 9000
# URL = f"https://movie.douban.com/subject/1291546/reviews?start={index}"
# while index < 9400:
#     URL = f"https://movie.douban.com/subject/1291546/reviews?start={index}"
#     print(index)
#     time.sleep(10)
#     total = scrape(URL, total)
#     index += 20
    
# print(total)
# with pd.ExcelWriter("Farewell My Concubine long reviews(9400).xlsx" , engine='xlsxwriter') as writer:
#     total.to_excel(writer, sheet_name = "Farewell My Concubine", index= False)
    
    
# total = pd.DataFrame(columns = ["Username", "Date/time of review","Rating of film", "Useful","Useless","Content"])
# index = 9400
# URL = f"https://movie.douban.com/subject/1291546/reviews?start={index}"
# while index < 9800:
#     URL = f"https://movie.douban.com/subject/1291546/reviews?start={index}"
#     print(index)
#     time.sleep(10)
#     total = scrape(URL, total)
#     index += 20
    
# print(total)
# with pd.ExcelWriter("Farewell My Concubine long reviews(9800).xlsx" , engine='xlsxwriter') as writer:
#     total.to_excel(writer, sheet_name = "Farewell My Concubine", index= False)
    
# total = pd.DataFrame(columns = ["Username", "Date/time of review","Rating of film", "Useful","Useless","Content"])
# index = 20
# URL = f"https://movie.douban.com/subject/1291546/reviews?start={index}"
# while index < 400:
#     URL = f"https://movie.douban.com/subject/1291546/reviews?start={index}"
#     print(index)
#     time.sleep(10)
#     total = scrape(URL, total)
#     index += 20
    
print(total)
with pd.ExcelWriter("Farewell My Concubine long reviews(20).xlsx" , engine='xlsxwriter') as writer:
    total.to_excel(writer, sheet_name = "Farewell My Concubine", index= False)
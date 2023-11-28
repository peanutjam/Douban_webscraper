# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 21:52:00 2023

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


def star(string):
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

total = pd.DataFrame(columns = ["Username", "Date/time of review", "Location of reviewer","Rating of film", "Popularity of review","Content"])

def scrape(URL, total):
    driver.get(URL)

    s = requests.session()
    selenium_user_agent = driver.execute_script("return navigator.userAgent")
    s.headers.update({"user-agent": selenium_user_agent})

    for cookie in driver.get_cookies():
        s.cookies.set(cookie["name"], cookie["value"], domain= cookie["domain"])
        
    response = s.get(URL)
    soup = BeautifulSoup(response.content, "html.parser")

    comments = soup.find_all("div", class_="comment")

    
    for comment in comments:
        user_name = comment.find("a", class_ ="")
        date = comment.find("span", class_ = "comment-time")
        location = comment.find("span", class_ = "comment-location")
        try:
            rating = comment.find("span", re.compile("allstar"))
        except:
            rating = None
        useful = comment.find("span", class_ = "votes vote-count")
        content = comment.find("span", class_ = "short")
        try:
            row = {"Username": user_name.text.strip(), 
                    "Date/time of review": date.text.strip() ,
                    "Location of reviewer" : location.text.strip(),  
                    "Rating of film" : star(rating.get("title")), 
                    "Popularity of review" : useful.text.strip(), 
                    "Content": content.text.strip() }
        except:
            row = {"Username": user_name.text.strip(), 
                    "Date/time of review": date.text.strip() ,
                    "Location of reviewer" : location.text.strip(),  
                    "Rating of film" : None, 
                    "Popularity of review" : useful.text.strip(), 
                    "Content": content.text.strip() }
        row = pd.DataFrame(row,index = [0])
        total = pd.concat([total,row], ignore_index = True)

        
    return total


driver = webdriver.Chrome()

driver.get("https://movie.douban.com/subject/1291546/comments?start=420&limit=20&status=P&sort=new_score")
driver.find_element(By.LINK_TEXT,"登录").click()
driver.find_element(By.LINK_TEXT,"wechat").click()
time.sleep(40)
driver.get("https://movie.douban.com/subject/1291546/comments?start=420&limit=20&status=P&sort=new_score")

fail = 0

URL = "https://movie.douban.com/subject/1291546/comments?start=20&limit=20&status=P&sort=new_score"

total = scrape(URL, total)


# for page 2 and beyond

index = 20

while index < 100:
    print(index)
    URL = f"https://movie.douban.com/subject/1291546/comments?start={index}&limit=20&status=P&sort=new_score"
    total = scrape(URL, total)
    index += 20

print(total)
print(fail)
with pd.ExcelWriter("Farewell My Concubine short reviews.xlsx") as writer:
    total.to_excel(writer, sheet_name = "Farewell My Concubine", index= False)

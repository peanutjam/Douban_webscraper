import requests
from bs4 import BeautifulSoup
import re
import xlrd
import pandas as pd
import time as time

total = pd.DataFrame(columns = ["Username", "Date/time of review", "Location of reviewer","Rating of film", "Popularity of review","Content"])
# URL = "https://movie.douban.com/subject/1291546/comments?sort=time&status=P"
URL = "https://movie.douban.com/subject/1291546/comments?start=420&limit=20&status=P&sort=new_score"
time.sleep(5)
headers = {
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
   }

page = requests.get(URL,headers=headers)
soup = BeautifulSoup(page.content, "html.parser")

comments = soup.find_all("div", class_="comment")
print(soup)

try:
    for comment in comments:
        user_name = comment.find("a", class_ ="")
        date = comment.find("span", class_ = "comment-time")
        location = comment.find("span", class_ = "comment-location")
        rating = comment.find("span", re.compile("allstar"))
        useful = comment.find("span", class_ = "votes vote-count")
        content = comment.find("span", class_ = "short")
        row = {"Username": user_name.text.strip(), 
                "Date/time of review": date.text.strip() ,
                "Location of reviewer" : location.text.strip(),  
                "Rating of film" : rating.get("title"), 
                "Popularity of review" : useful.text.strip(), 
                "Content": content.text.strip() }
        total = total.append(row, ignore_index = True)
except:
    print (user_name, date, location,rating,useful,content)

print(total)

# print(comments)


#for page 2 and beyond

# index = 20

# while index < 240:
#     print(index)
#     URL = f"https://movie.douban.com/subject/1291546/comments?start={index}&limit=20&status=P&sort=time"
#     headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
#     }

#     page = requests.get(URL,headers=headers)
#     print(page.status_code)
#     soup = BeautifulSoup(page.content, "html.parser")

#     comments = soup.find_all("div", class_="comment")


#     try:
#         for comment in comments:
#             user_name = comment.find("a", class_ ="")
#             date = comment.find("span", class_ = "comment-time")
#             location = comment.find("span", class_ = "comment-location")
#             rating = comment.find("span", re.compile("allstar"))
#             useful = comment.find("span", class_ = "votes vote-count")
#             content = comment.find("span", class_ = "short")
#             row = {"Username": user_name.text.strip(), 
#                     "Date/time of review": date.text.strip() ,
#                     "Location of reviewer" : location.text.strip(),  
#                     "Rating of film" : rating.get("title"), 
#                     "Popularity of review" : useful.text.strip(), 
#                     "Content": content.text.strip() }
#             total = total.append(row, ignore_index = True)
#     except:
#         print(index, user_name, date, location,rating,useful,content)
#     index += 20

# print(total)

# with pd.ExcelWriter("Farewell My Concubine.xlsx") as writer:
#     total.to_excel(writer, sheet_name = "Farewell My Concubine", index= False)
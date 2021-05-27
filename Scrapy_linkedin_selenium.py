import urllib
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
import sys
import json
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

if sys.version_info[0] < 3:
    print('Sorry, Python 3 only for now...')
    exit()

browser = webdriver.Chrome()
# linkedin登陆页面
url = r'https://www.twitter.com/usnavy'
browser.get(url)


# 输入用户名
username = browser.find_element_by_name('session_key')
username.send_keys('email')
# 输入密码
password = browser.find_element_by_name('session_password')
password.send_keys('password')

browser.find_element_by_name('signin').send_keys(Keys.ENTER)

browser.implicitly_wait(3)


def getCompanyInfo(CompanyName):
    URL = 'https://linkedin.com' + CompanyName
    print('Start scarping information of : ',URL)
    browser.implicitly_wait(15)
   
    name = " "
    description = " "
    website = " "
    address = " "
    founded_time = " "
    crawl = " "

    try:
      company_name = bs.find('h1',class_= re.compile('org-top-card-module__name'))
      name = company_name.text
      name = name.strip()
    except:
       print('could not find the company name!')
    try:
      
      company_description = bs.find('p', class_=re.compile('description__text'))
      description = company_description.text
      description = description.strip()
    except:
      print('could not find the company description!')
    try:
      
      company_website = bs.find("a", href=re.compile("^(http|www)"))
      website = company_website.text
      website = website.strip()

    except:
      print("could not find the company's website")
    try:
      
      company_address = bs.find('p', class_=re.compile('company-module__headquarters'))
      address = company_address.text
      address = address.strip()
    except:
      print("could not find the company's website!")
    try:
     
      company_founded_time = bs.find("p", class_=re.compile("company-module__founded"))
      founded_time = company_founded_time.text
      founded_time = founded_time.strip()
    except:
      print("could not find the company's founded time!")
    try:
      
      staff_number = bs.find('p', class_=re.compile('company-module__company-staff-count-range'))
      crawl = staff_number.text
      crawl = crawl.strip()
    except:
       print("could not find the company's staff_number!")

    company = {
        'Company_ID':CompanyName,
        'Company_name': name,
        'Company_description': description,
        'Company_website': website,
        'Company_address': address,
        'Time_founded': founded_time,
        'Crawl_number': crawl
      }

    with open('results.txt', 'a') as f:
          f.write(json.dumps(company)+'\r\n')

#获取某公司页面中的相似公司，返回相似公司的域名尾部
def getSimilarCompany(Cpname):
  startURL= 'https://linkedin.com' + Cpname
  print('Start scraping the similar companies of',Cpname,':',startURL)
  browser.get(startURL)
  
  browser.implicitly_wait(15)
  companySet = []
  global bs
  pageSource = browser.page_source.encode('utf-8')
  bs = BeautifulSoup(pageSource, "lxml")
  names = bs.find_all('a',class_=re.compile('link-without-hover-state'))
  
  for name in names:
      bmp = name.attrs['href']
      bmp.strip()
      companySet.append(bmp)
  print('the similar companies of',Cpname,'are:',companySet)
  return companySet

if __name__ == '__main__':
    #目前搜索深度只能设置为偶数
    global searchDepth
    searchDepth = 10
    print('start scraping!\n')
    list3=[]
    with open('results.txt', 'rb') as f:
        for line in f:
            setting = json.loads(line.strip())
            list3.append(setting['Company_ID'])
    list1 = []
    list2 = []
    StartCompany = '/company/google'
    list1 = getSimilarCompany(StartCompany)
    getCompanyInfo(StartCompany)

    while searchDepth >= 0:
        searchDepth = searchDepth - 1

        if searchDepth%2 == 1:
          for name in list1:
             if name in list3 :
                  continue
             else:
                  list3.append(name)
                  list2.extend(getSimilarCompany(name))
                  getCompanyInfo(name)
          list1 = []
        else:
          for name in list2:
              if name in list3:
                  continue
              else:
                  list3.append(name)
                  list1.extend(getSimilarCompany(name))
                  getCompanyInfo(name)
          list2 = []
    browser.close()

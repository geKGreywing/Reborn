
##載入所需函式
from selenium import webdriver
import time
import datetime
import keyboard 
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options as ChromeOptions

##設定webdriver 防止它自動關閉
options = ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument("--disable-notifications")
driver2 = webdriver.Chrome('./chromedriver',options=options)




def login():

    ##登入股票大富翁
    driver2.get('https://www.cmoney.tw/member/login/')
    account = driver2.find_element("xpath",'//*[@id="Account"]')
    account.clear()
    account.send_keys("***@gmail.com")
    password = driver2.find_element("xpath",'//*[@id="Password"]') #網頁的密碼點
    password.clear()
    password.send_keys("***password")
    time.sleep(1)
    driver2.find_element("xpath",'//*[@id="Login"]').click()
    time.sleep(1)

    ##繞過雙重驗證
    driver2.find_element("xpath",'//*[@id="Form"]/div[2]/div/button[1]').click()
    time.sleep(5)

    ##前往首頁
    driver2.get('https://www.cmoney.tw/vt/main-page.aspx?aid=*****#Al')


def buy(a):##以482塊下單2330一張
    stock = driver2.find_element("xpath",'//*[@id="textBoxCommkey"]')
    stock.clear()
    stock.send_keys("2330")
    amount = driver2.find_element("xpath",'//*[@id="TextBoxQty"]')
    amount.clear()
    amount.send_keys(a)
    driver2.find_element("xpath",'//*[@id="AccountOrderSelect"]/ul/li[2]/a').click()
    time.sleep(0.5)
    driver2.find_element("xpath",'//*[@id="pricepicker"]/a[1]').click()
    time.sleep(0.5)
    driver2.find_element("xpath",'//*[@id="Orderbtn"]').click()
    time.sleep(0.5)

def sell(a):##以482塊下單2330一張
    stock = driver2.find_element("xpath",'//*[@id="textBoxCommkey"]')
    stock.clear()
    stock.send_keys("2330")
    amount = driver2.find_element("xpath",'//*[@id="TextBoxQty"]')
    amount.clear()
    amount.send_keys(a)
    driver2.find_element("xpath",'//*[@id="AccountOrderSelect"]/ul/li[3]/a').click()
    time.sleep(0.5)
    driver2.find_element("xpath",'//*[@id="pricepicker"]/a[1]').click()
    time.sleep(0.5)
    driver2.find_element("xpath",'//*[@id="Orderbtn"]').click()
    time.sleep(0.5)

def pricecheck2330():
    response = requests.get("https://tw.stock.yahoo.com/quote/2330")
    soup = BeautifulSoup(response.text, 'lxml')
    try:
        price2330 = soup.find('span', {'class': 'Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-up)'}).getText()
    except:
        price2330 = soup.find('span', {'class': 'Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-down)'}).getText()
    return float(price2330)

def hrcatch():
    time.sleep(1)
    hr = datetime.datetime.now().strftime('%H')
    hr=int(hr)
    return hr
    

    
def mncatch():
    time.sleep(1)
    mn = datetime.datetime.now().strftime('%M')
    mn=int(mn)
    return mn

login()
pricecheck2330()
time.sleep(15)
hr = 8
mn = 59
sc = 0
while True:
    time.sleep(1)
    sc += 1
    if sc == 60:
        mn+=1
        sc=0

    if mn == 60:
        hr+=1
        mn=0

    if hr == 9:
        if mn == 0:
            break
    print(f'time is {hr}:{mn}:{sc}')

driver2.get('https://www.cmoney.tw/vt/main-page.aspx?aid=***#Al')
status=0 ## 0開盤 1跌破開盤 2站回開盤+買進 3賣出第一張(2%) 4賣出第二章(4%) 5賣出第二章(0%)
#while True:
   # time.sleep(1)
   # try:
      #  first = pricecheck2330()
     #   print(first)
    #    break
   # except:
    #    print('failed')
first = 476.5
price2330 = 476.5




while True:
    print(status)
    time.sleep(1)
    print(f'time is {hr}:{mn}:{sc}')
    sc += 1
    if sc == 60:
        mn+=1
        sc=0
    if mn == 60:
        hr+=1
        mn=0
    if hr==9 and mn==1 and sc==30:
        price2330=476.5
    elif hr==9 and mn==2 and sc==29:
        price2330=477.0
    elif hr==9 and mn==3 and sc==0:
        price2330=477.5
    elif hr==9 and mn==4 and sc==0:
        price2330=475.0
    elif hr==9 and mn==4 and sc==49:
        price2330=476.5
    elif hr==9 and mn==5 and sc==0:
        price2330=475.5
    elif hr==9 and mn==5 and sc==14:
        price2330=476.0
    elif hr==9 and mn==5 and sc==30:
        price2330=475.0
    else:
        pass

    print(f'now price is {price2330}')
    if price2330<first and status==0: 
        status =1
    elif price2330>first and status==0: 
        status =-1
    elif price2330 >= first and status==1:
        #money = driver2.find_element("xpath",'//*[@id="TabContent"]/div/div/div[2]/table/tbody/tr[1]/td').text
       # money=money.replace(",","")
        #money=int(money[2:])
       # print(money)
       # if money>2*price2330*1000:
        buy(2)
        status =2
    elif price2330 <= first and status==-1:
        sell(2) 
        status =-2


    if status >=2 and status <4:
        if price2330>=first*(1.002):
            sell(1)
            status = 3
        if status==3:
            if price2330>=first*(1.004):
                sell(1)
                status = 4
            if price2330==first:
                sell(1)
                status = 5
        else:
            if price2330<=first*(0.996):
                sell(2)
                status =6


    if status <=-2 and status >-4:
        if price2330<=first*(0.998):
            buy(1)
            status = -3
        if status==-3:
            if price2330<=first*(0.996):
                buy(1)
                status = -4
            if price2330==first:
                buy(1)
                status = -5
        else:
            if price2330<=first*(1.004):
                buy(2)
                status =-6


    if hr ==13 and mn>=20:
        if status == 2:
            sell(2)
        elif status <7 and status >=3:
            sell(1)
        if status == -2:
            buy(2)
        if status >-7 and status <=-3:
            buy(1)
        status =7

    if status >=4 or status <=-4:
        driver2.quit()
        break


        
                
        
            

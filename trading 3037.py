
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
driver = webdriver.Chrome('./chromedriver',options=options)




def login():

    ##登入股票大富翁
    driver.get('https://www.cmoney.tw/member/login/')
    account = driver.find_element("xpath",'//*[@id="Account"]')
    account.clear()
    account.send_keys("***@gmail.com")
    password = driver.find_element("xpath",'//*[@id="Password"]') #網頁的密碼點
    password.clear()
    password.send_keys("***password")
    time.sleep(1)
    driver.find_element("xpath",'//*[@id="Login"]').click()
    time.sleep(1)

    ##繞過雙重驗證
    try:
        driver.find_element("xpath",'//*[@id="Form"]/div[2]/div/button[1]').click()
    except:
        pass
    time.sleep(2)

    ##前往首頁
    driver.get('https://www.cmoney.tw/vt/main-page.aspx?aid=***#Al')


def buy(a):##以482塊下單2330一張
    stock = driver.find_element("xpath",'//*[@id="textBoxCommkey"]')
    stock.clear()
    stock.send_keys("3037")
    amount = driver.find_element("xpath",'//*[@id="TextBoxQty"]')
    amount.clear()
    amount.send_keys(a)
    driver.find_element("xpath",'//*[@id="AccountOrderSelect"]/ul/li[2]/a').click()
    time.sleep(0.5)
    driver.find_element("xpath",'//*[@id="pricepicker"]/a[1]').click()
    time.sleep(0.5)
    driver.find_element("xpath",'//*[@id="Orderbtn"]').click()
    time.sleep(0.5)

def sell(a):##以482塊下單2330一張
    stock = driver.find_element("xpath",'//*[@id="textBoxCommkey"]')
    stock.clear()
    stock.send_keys("3037")
    amount = driver.find_element("xpath",'//*[@id="TextBoxQty"]')
    amount.clear()
    amount.send_keys(a)
    driver.find_element("xpath",'//*[@id="AccountOrderSelect"]/ul/li[3]/a').click()
    time.sleep(0.5)
    driver.find_element("xpath",'//*[@id="pricepicker"]/a[1]').click()
    time.sleep(0.5)
    driver.find_element("xpath",'//*[@id="Orderbtn"]').click()
    time.sleep(0.5)

def pricecheck():
    global price1
    response = requests.get("https://tw.stock.yahoo.com/quote/3037")
    soup = BeautifulSoup(response.text, 'lxml')
    try:
        price1 = soup.find('span', {'class': 'Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-up)'}).getText()
        return float(price1)
    except:
        pass

    try:
        price1 = soup.find('span', {'class': 'Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-down)'}).getText()
        return float(price1)
    except:
        pass

    try:
        price1 = soup.find('span', {'class': 'Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c)'}).getText()
        return float(price1)
    except:
        pass

    try:
        price1 = soup.find('span', {'class': 'Fz(32px) Fw(b) Lh(1) Mend(16px) C(#fff) Px(6px) Py(2px) Bdrs(4px) Bgc($c-trend-up)'}).getText() ##漲停
        return float(price1)
    except:
        pass

    print("error here")
    return float(price1)

def hrcatch():
    hr = datetime.datetime.now().strftime('%H')
    hr=int(hr)
    return hr

def mncatch():
    mn = datetime.datetime.now().strftime('%M')
    mn=int(mn)
    return mn
    


login()
time.sleep(15)
driver.get('https://www.cmoney.tw/vt/main-page.aspx?aid=***#Al')
while True:
    time.sleep(1)
    hr=hrcatch()
    mn=mncatch()
    print(f'time is {hr}:{mn}')
    if hr == 9:
        if mn == 0:
            break


status=0 ## 0開盤 1跌破開盤 2站回開盤+買進 3賣出第一張(2%) 4賣出第二章(4%) 5賣出第二章(0%)
while True:
    try:
        first = pricecheck()
        print(first)
        break
    except:
        print('failed')
    time.sleep(1)

while True:
    time.sleep(60)
    print(f'status is {status}')
    hr=hrcatch()
    mn=mncatch()
    print(f'time is {hr}:{mn}')
    price2330 = pricecheck() #抓時間+股價
    print(f'now price is {price2330}')
    if price2330<first and status==0: 
        status =1
    elif price2330>first and status==0: 
        status =-1
    elif price2330 >= first and status==1:
        buy(6)
        status =2
    elif price2330 <= first and status==-1:
        sell(6) 
        status =-2

    if status >=2 and status <4:
        if price2330>=first*(1.02) and status == 2:
            sell(3)
            status = 3
        if status==3:
            if price2330>=first*(1.04):
                sell(3)
                status = 4
            if price2330<=first:
                sell(3)
                status = 5
        else:
            if price2330<=first*(0.98):
                sell(6)
                status =6

    if status <=-2 and status >-4:
        if price2330<=first*(0.98) and status==-2:
            buy(3)
            status = -3
        if status==-3:
            if price2330<=first*(0.96):
                buy(3)
                status = -4
            if price2330==first:
                buy(3)
                status = -5
        else:
            if price2330>=first*(1.02):
                buy(6)
                status =-6

    if hr ==13 and mn>=20:
        if status == 2:
            sell(6)
        elif status <7 and status >=3:
            sell(3)
        if status == -2:
            buy(6)
        elif status >-7 and status <=-3:
            buy(3)
        status =7

    if status >=4  or status <=-4:
        print(status)
        driver.quit()
        break


        
                
        
            

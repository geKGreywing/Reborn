
##載入所需函式
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time
import datetime
import keyboard 
import requests
from bs4 import BeautifulSoup


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
    driver.find_element("xpath",'//*[@id="Form"]/div[2]/div/button[1]').click()
    time.sleep(2)

    ##前往首頁
    driver.get('https://www.cmoney.tw/vt/main-page.aspx?aid=***#Al')


def buy(a):
    stock = driver.find_element("xpath",'//*[@id="textBoxCommkey"]')
    stock.clear()
    stock.send_keys("3362")
    amount = driver.find_element("xpath",'//*[@id="TextBoxQty"]')
    amount.clear()
    amount.send_keys(a)
    driver.find_element("xpath",'//*[@id="AccountOrderSelect"]/ul/li[2]/a').click()
    time.sleep(0.5)
    driver.find_element("xpath",'//*[@id="pricepicker"]/a[1]').click()
    time.sleep(0.5)
    driver.find_element("xpath",'//*[@id="Orderbtn"]').click()
    time.sleep(0.5)

def sell(a):
    stock = driver.find_element("xpath",'//*[@id="textBoxCommkey"]')
    stock.clear()
    stock.send_keys("3362")
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
    global price
    response = requests.get("https://tw.stock.yahoo.com/quote/3362")
    soup = BeautifulSoup(response.text, 'lxml')
    
    try:
        price = soup.find('span', {'class': 'Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-up)'}).getText() ##上漲
        return float(price)
    except:
        pass
    try:
        price = soup.find('span', {'class': 'Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-down)'}).getText() ##下跌
        return float(price)
    except:
        pass
    try:
        price = soup.find('span', {'class': 'Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c)'}).getText() ##持平
        return float(price)
    except:
        pass

    try:
        price1 = soup.find('span', {'class': 'Fz(32px) Fw(b) Lh(1) Mend(16px) C(#fff) Px(6px) Py(2px) Bdrs(4px) Bgc($c-trend-up)'}).getText() ##漲停
        return float(price)
    except:
        pass
    try:
        price1 = soup.find('span', {'class': 'Fz(32px) Fw(b) Lh(1) Mend(16px) C(#fff) Px(6px) Py(2px) Bdrs(4px) Bgc($c-trend-down)'}).getText() ##跌停
        return float(price1)
    except:
        pass
    print("error here")
    return float(price)

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


status=0
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
    price3362 = pricecheck() #抓時間+股價
    print(f'now price is {price3362}')
    if price3362<first and status==0: 
        status =1
    elif price3362>first and status==0: 
        status =-1
    elif price3362 >= first and status==1:
        buy(10)
        status =2
    elif price3362 <= first and status==-1:
        sell(10) 
        status =-2

    if status >=2 and status <4:
        if price3362>=first*(1.04) and status == 2:
            sell(5)
            status = 3
        if status==3:
            if price3362>=first*(1.08):
                sell(5)
                status = 4
            if price3362<=first:
                sell(5)
                status = 5
        else:
            if price3362<=first*(0.96):
                sell(10)
                status =6

    if status <=-2 and status >-4:
        if price3362<=first*(0.96) and status==-2:
            buy(5)
            status = -3
        if status==-3:
            if price3362<=first*(0.92):
                buy(5)
                status = -4
            if price3362==first:
                buy(5)
                status = -5
        else:
            if price3362>=first*(1.04):
                buy(10)
                status =-6

    if hr ==13 and mn>=20:
        if status == 2:
            sell(10)
        elif status <7 and status >=3:
            sell(5)
        if status == -2:
            buy(10)
        elif status >-7 and status <=-3:
            buy(5)
        status =7

    if status >=4 or status <=-4 or keyboard.is_pressed("q"):
        print(status)
        driver.quit()
        break


        
                
        
            

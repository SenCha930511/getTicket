from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import requests
from ftplib import FTP
import time
import random

reseveTime = "2022-11-18"

while 1:
    try:
        service = Service("D:/workspace/python/ticket/chromedriver/chromedriver.exe")
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument(f'--remote-debugging-port={random.randint(10000, 60000)}')

        driver = webdriver.Chrome(service = service, options = options)

        driver.get("https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query")

        time.sleep(1)

        driver.find_element("css selector", "#pid").send_keys("A160836036")
        driver.find_element("css selector", "#queryForm > div.basic-info > div:nth-child(3) > div.btn-group > label:nth-child(2)").click()
        driver.find_element("css selector", "#startStation1").send_keys("3300")
        driver.find_element("css selector", "#endStation1").send_keys("1020")
        driver.find_element("css selector", "#rideDate1").clear()
        driver.find_element("css selector", "#rideDate1").send_keys("".join(reseveTime.split("-")))
        start = Select(driver.find_element("css selector", "#startTime1"))
        start.select_by_value("16:00")
        end = Select(driver.find_element("css selector", "#endTime1"))
        end.select_by_value("23:00")
        driver.find_element("css selector", "#queryForm > div:nth-child(3) > div.column.byTime > div > div.trainType > label:nth-child(1)").click()
        driver.find_element("css selector", "#queryForm > div:nth-child(3) > div.column.byTime > div > div.trainType > label:nth-child(2)").click()
        driver.find_element("css selector", "#queryForm > div:nth-child(3) > div.column.byTime > div > div.trainType > label:nth-child(3)").click()
        driver.find_element("css selector", "#queryForm > div:nth-child(3) > div.column.byTime > div > div.trainType > label:nth-child(4)").click()
        driver.find_element("css selector", "#queryForm > div:nth-child(3) > div.column.byTime > div > div.trainType > label:nth-child(5)").click()
        driver.find_element("css selector", "#queryForm > div:nth-child(3) > div.column.byTime > div > div.trainType > label:nth-child(6)").click()
        driver.find_element("css selector", "#queryForm > div.btn-sentgroup > input").click()
        pageSource = driver.page_source
        soup = BeautifulSoup(pageSource, "html.parser")

        result = soup.find("div", {"class": "alert alert-info"}).text

        if "????????????" in result:
            print(f"<{time.strftime('%Y-%m-%d %I:%M:%S %p', time.localtime())}> ????????????")
        else:
            print(f"<{time.strftime('%Y-%m-%d %I:%M:%S %p', time.localtime())}> ????????????\n")
            infos = soup.find_all("tr", {"class": "trip-column"})
            allTrains = []
            for info in range(0, len(infos)):
                for d in str(infos[info]).split("<!--"):
                    if "????????????" in d:
                        allTrains.append([d.split('(???????????????)">')[1][:-11]])
                    if "????????????" in d:
                        allTrains[info].append(d.split("<td>")[1][:5])
                        allTrains[info].append(d.split("<td>")[2][:5])
                        allTrains[info].append(d.split("<td>")[3][:-6])
                        allTrains[info].append(d.split("<td>")[4][:-6])
                    if "???????????????" in d:
                        allTrains[info].append(d.split("<td>")[1][:5])

            message = ""
            for i in range(0, len(allTrains)):
                message = message + f"{i+1}. ??????: {allTrains[i][0]}, ????????????: {allTrains[i][1]}, ????????????: {allTrains[i][2]}, ????????????: {allTrains[i][3]}, {allTrains[i][4]}, ??????: {allTrains[i][5]}\n"
            message = f"???{reseveTime} ????????? {len(allTrains)} ?????????\n{message}"
            print(message)
  
            with open("D:/workspace/python/ticket/ticket.txt", "w", encoding = "utf-8") as f:
                f.write(message)

            ftp = FTP("sencha.xyz")
            ftp.login("", "")
            ftp.cwd("/home")
            f = open("D:/workspace/python/ticket/ticket.txt", "rb")
            ftp.storbinary("STOR ticket.txt", f, 1024)
            ftp.quit()
            f.close()
            
            url = "https://senchaaa.uk:5050/notify"

            if "????????? 288" in message: 
                headers = {"X-Message":  "success"}
                r = requests.post(url, headers = headers)
                print(r.status_code)

        driver.quit()
        time.sleep(60)

    except Exception as e:
        print(e)


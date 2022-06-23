from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
from selenium.webdriver.chrome.service import Service
from unidecode import unidecode

class Divar():
    def __init__(self):
        self.url="https://divar.ir/s/tehran/rent-residential"
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        s=Service('/home/hamed/project/learn/home_predict/chromedriver')
        self.driver1 =  webdriver.Chrome(service=s,options=op)
        self.driver1.get(self.url)
        self.driver2 =  webdriver.Chrome(service=s,options=op)
        self.run()


    def get_floor(self, row):
        floor_all = row.find_elements(By.XPATH,value=".//p[@class = 'kt-unexpandable-row__value']")[0].text
        floor= floor_all.split("از")[0]
        if (floor == "همکف"):
            floor = 0
        elif (floor == "زیرهمکف"):
            floor = -1
        else :
            floor = int(unidecode(floor))
        return floor

    def get_place(self):
        rows =  self.driver2.find_elements(By.XPATH,value="//div[@class = 'kt-page-title__subtitle kt-page-title__subtitle--responsive-sized']")
        text = rows[0].text
        sp = text.split('،')
        city = sp[0].split()[-1]
        region = sp[1].split("|")[0]
        return city, region


    def get_deposit(self, row):
        deposit_all = row.find_elements(By.XPATH,value=".//p[@class = 'kt-unexpandable-row__value']")[0].text
        deposit= deposit_all.split(" ")[0]
        if deposit == "توافقی":
            deposit = -100
        elif deposit == "مجانی":
            deposit = 0
        else :
            deposit = int(unidecode(deposit).replace(",",""))
        return deposit


    def get_rent(self, row):
        rent_all = row.find_elements(By.XPATH,value=".//p[@class = 'kt-unexpandable-row__value']")[0].text
        rent= rent_all.split(" ")[0]
        if rent == "توافقی":
            rent = -100
        elif rent == "مجانی":
            rent = 0
        else :
            rent = int(unidecode(rent).replace(",",""))
        return rent


    def get_one_home_info(self, url):
        rent = -100
        deposit = -100
        floor = -100
        self.driver2.get(url)
        rows =  self.driver2.find_elements(By.XPATH,value="//div[@class = 'kt-base-row kt-base-row--large kt-unexpandable-row']")
        for row in rows:
            row_name = row.find_elements(By.XPATH,value=".//p[@class = 'kt-base-row__title kt-unexpandable-row__title']")[0].text
            if row_name == "طبقه":
                floor = self.get_floor(row)
            if row_name == "ودیعه":
                deposit = self.get_deposit(row)
            if row_name == "اجارهٔ ماهانه":
                rent = self.get_rent(row)
        city, region = self.get_place()
        column = self.driver2.find_elements(By.XPATH,value="//span[@class = 'kt-group-row-item__value']")
        area = int(unidecode(column[0].text))
        age = int(unidecode(column[1].text.split()[-1]))
        if(column[2].text == "بدون اتاق"):
            rooms = 0
        else:
            rooms = int(unidecode(column[2].text))
        print(f"deposit : {deposit}  , rent : {rent}  , floor : {floor} , area : {area} , age : {age} , rooms : {rooms} , city : {city}, region : {region}")
        

    def run(self):
        all_results =self.driver1.find_elements(By.XPATH,value="//section[@class = 'post-card-item kt-col-6 kt-col-xxl-4']")
        for result in all_results:
            href_class_1 = result.find_elements(By.XPATH,value="./a[@class = 'kt-post-card kt-post-card--outlined']")
            href_class_2 = result.find_elements(By.XPATH,value="./a[@class = 'kt-post-card kt-post-card--outlined kt-post-card--has-chat']")

            address = href_class_1 if href_class_1 != [] else href_class_2
            self.get_one_home_info(address[0].get_attribute('href'))
    

if __name__ == "__main__":
    Divar()
from selenium import webdriver
import time 
import sys
import os

class Finder:
    def __init__(self, *args, **kwargs):
        self.server_name = kwargs['server_name']
        self.password = kwargs['password']
        self.interface_name = kwargs['interface']
        self.main_dict = {}

    def run(self):
        command = """sudo iwlist wlp1s0 scan | grep -ioE 'ssid:"(.*{}.*)'"""
        result = os.popen(command.format(self.server_name))
        result = list(result)

        if "Device or resource busy" in result:
                return None
        else:
            ssid_list = [item.lstrip('SSID:').strip('"\n') for item in result]
            print("Successfully get ssids {}".format(str(ssid_list)))

        for name in ssid_list:
            try:
                result = self.connection(name)
            except Exception as exp:
                print("Couldn't connect to name : {}. {}".format(name, exp))
            else:
                if result:
                    print("Successfully connected to {}".format(name))
                    return True

    def connection(self, name):
        try:
            os.system("nmcli d wifi connect {} password {} iface {}".format(name,
       self.password,
       self.interface_name))
        except:
            raise
        else:
            return True

def Activate_wifi(wifiName,Password):
    interface_name = "wlp1s0"
    F = Finder(server_name=wifiName,
               password=Password,
               interface=interface_name)
    return F.run()

def login(Username):
    chromedriver_location = "./chromedriver"
    driver = webdriver.Chrome(chromedriver_location)
    driver.get('http://10.0.4.12:8090/')
    username = '//*[@id="username"]'
    password = '//*[@id="password"]'
    submit = '/html/body/div[2]/div[1]/div[2]/div[2]/a'
    time.sleep(1)
    driver.find_element_by_xpath(username).send_keys(username)
    driver.find_element_by_xpath(password).send_keys(username)
    driver.find_element_by_xpath(submit).click()
    time.sleep(1)
    driver.quit()

def main():
    file = open('./cred.txt', 'r') 
    lines = file.readlines()  
    lines = [ line.strip() for line in lines ]
    Username = lines[0]
    wifiName = lines[1]
    Password = lines[2]

    while(True):
        if(Activate_wifi(wifiName,Password)):
            login(Username)
            break

if __name__=="__main__":
    main()

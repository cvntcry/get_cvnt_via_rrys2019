#!/usr/bin/python3
# coding:utf-8


import requests
import json
import time


class SaveData:
  def __init__(self):
    self.headers = {
      "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36 OPR/55.0.2994.61",
      "Accept":"application/json, text/javascript, */*; q=0.01"
    }
    self.uids = set()

  def enumerateUid(self):
    print("**start program**")
    time.sleep(2)
    print("enumerate all uids...")
    for num in range(1,10000001):
      self.uids.add(num)
    print("aim {} uids...".format(len(self.uids)))

  def exposureUid(self):
    time.sleep(2)
    print("check all valid uids...")
    with open("jsondata.txt","a",encoding="utf-8") as f:
      for uid in self.uids:
        url = "http://www.rrys2019.com/user/index/getinfo?uid={}".format(uid)
        while True:
          try:
            response = requests.get(url,headers=self.headers)
          except Exception as e:
            time.sleep(2)
            continue
          if response.status_code == 200:
            break
          else:
            print("502...")
            time.sleep(2)
            continue
        html = response.content.decode()
        if "uid" in html:
          f.write(html)
          f.write("\n")
    print("checked all uids...")

  def checkResult(self):
    time.sleep(2)
    print("read jsondata.txt to validusers.txt...")
    try:
      with open("validusers.txt","a",encoding="utf-8") as p:
        with open("jsondata.txt","r",encoding="utf-8") as f:
          l = 1
          while l:
            l = f.readline()
            infos = l.split("\n")
            if len(infos) == 2:
              info = infos[0]
              if info != "":
                html = json.loads(info)
                uid = html["data"]["uid"]
                nickname = html["data"]["nickname"]
                group = html["data"]["main_group_name"]
                user = uid + "  :  " + nickname + "  :  " + group
                p.write(user + "\n")
            elif len(infos) > 2:
              with open("bugnickname.txt","a",encoding="utf-8") as b:
                b.write(l)
              continue             
    except Exception as e:
      print("check result error...")
    print("**end program**")

  def run(self):
    self.enumerateUid()
    self.exposureUid()
    self.checkResult()


if __name__ == "__main__":
  save = SaveData()
  save.run()


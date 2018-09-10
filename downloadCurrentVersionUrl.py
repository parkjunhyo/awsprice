#! /usr/bin/env python

import os, sys, re, shutil
import json
import subprocess

class Main:

 offercodejson={}

 def getOfferCodeAPItarget(self):
    f = open("getOfferCode.sh", 'r')
    rcont = f.readlines()
    f.close()
    for rd in rcont:
       if re.search("offercodeapitarget=", rd):
         return rd.strip().split("=")[-1].split("\"")[1]
         break

 def checkOffercodeExist(self):
    if not os.path.isfile("./offercodes/index.json"):
      print "Error:1: no index.json in offercodes directory, run getOfferCode.sh before"
      sys.exit()

 def cleandirectory(self, dirname, currntversioninfo):
    subdirnamelist = currntversioninfo.keys()
    if not len(subdirnamelist):
      shutil.rmtree(dirname) 
      return 
    if os.path.isdir(dirname):
      shutil.rmtree(dirname)
    os.mkdir(dirname)
    # create subdirectoy
    for sn in subdirnamelist:
       path = dirname + "/" + sn
       os.makedirs(path)
       #
       runfile = path + "/downloadrun.sh"
       writemsg = "wget "+currntversioninfo[sn]
       #
       ltemp = writemsg.strip().split('.')[:-1]
       ltemp.append(u'csv')
       csvdown = '.'.join(ltemp)
       #
       f = open(runfile, 'w')
       f.write("#! /usr/bin/env bash\n")
       f.write(writemsg+"\n")
       f.write(csvdown+"\n")
       f.close()
       os.chmod(runfile, 0777) 

 def readOfferCodeIndexJson(self):
    f = open("./offercodes/index.json", 'r')
    rcont = f.read()
    f.close()
    temp = json.loads(rcont)
    self.offercodejson = temp[u'offers']
    # 
    offerCodeAPItargetURL = self.getOfferCodeAPItarget()
    #
    currntversioninfo = {}
    offercodekeyslist = self.offercodejson.keys()
    for srvn in offercodekeyslist:
       if srvn not in currntversioninfo.keys():
         currntversioninfo[srvn] = offerCodeAPItargetURL+self.offercodejson[srvn][u'currentVersionUrl']
    #
    dirname = "./currentversions"
    self.cleandirectory(dirname, currntversioninfo)
    #
    currentdirn = os.getcwd()
    for srvn in currntversioninfo.keys():
       chdirn = currentdirn + "/currentversions/" + srvn
       os.chdir(chdirn)
       os.system("./downloadrun.sh&")
       os.chdir(currentdirn)

 def __init__(self, argv):
   pass

 def runInstance(self):
   self.checkOffercodeExist()
   self.readOfferCodeIndexJson()

if __name__ == "__main__":
  m = Main(sys.argv)
  m.runInstance();

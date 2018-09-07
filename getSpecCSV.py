#! /usr/bin/env python

import sys, os, re
import json
from multiprocessing import Process


class Main:

     currdirectory = os.getcwd()
     targetdirname = currdirectory+"/currentversions"
     listindirectory = os.listdir(targetdirname)

     def checkcurrentversionsdirectory(self):
        if not os.path.isdir(self.targetdirname):
          print "Error:1: not currentversions directory, run downloadCurrentVersionUrl.py before"
          sys.exit()
        if not len(self.listindirectory):
          print "Error:2: not currentversions directory, run downloadCurrentVersionUrl.py before"
          sys.exit()

     def __init__(self, argv):
        self.checkcurrentversionsdirectory()

     
     def analysisindexjson(self, tardir):
        os.chdir(tardir)
        runfile = tardir + "/downloadrun.sh"
        currfile = tardir + "/index.json"
        if not os.path.isfile(currfile):
          os.system(runfile)
        f = open(currfile)
        rcont = f.read()
        f.close()
        temp = json.loads(rcont)
        # 
        print temp.keys()
        #
        #offerCoden = temp[u'offerCode']
        #
        #versionn = temp[u'version']
        #
        #productsn = temp[u'products']
        #
        #termsn = temp[u'terms']
        # 
        os.chdir(self.currdirectory)

     def runInstance(self):
        processlist = []
        for srvn in self.listindirectory:
           tardir =  self.targetdirname + "/" + srvn
           if os.path.isdir(tardir):
             proc = Process(target = self.analysisindexjson, args = (tardir,)) 
             if proc not in processlist:
               proc.start()
               processlist.append(proc)
        for proc in processlist:
           proc.join()
   

   

if __name__ == "__main__":
  m = Main(sys.argv)
  m.runInstance()

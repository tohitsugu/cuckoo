#!/usr/bin/env python                                                                                                                                

import pyinotify                                                                    
import fnmatch                                                                      
import os

wm = pyinotify.WatchManager()  # Watch Manager
mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE  # watched events

remotehost = "10.30.0.87"
remotefile = "/home/tohitsugu/cuckoo/testing/"

def suffix_filter(fn):                                                              
    suffixes = ["*.clean", "*.clean.*"]                                                                                                                
    for suffix in suffixes:                                                         
        if fnmatch.fnmatch(fn, suffix):                                             
            return False                                                            
    return True                                                                     

class EventHandler(pyinotify.ProcessEvent):                                         
    def process_IN_CREATE(self, event):                                             
        if  suffix_filter(event.name):                                           
            print "Creating:", event.pathname                                       
   	    localfile = event.pathname
            print "Transferring:", event.pathname	
            os.system('scp "%s" tohitsugu@"%s:%s"' % (localfile, remotehost, remotefile) )




    def process_IN_DELETE(self, event):                                             
        if  suffix_filter(event.name):                                           
            print "Removing:", event.pathname                                       

    def process_IN_MODIFY(self, event):                                             
        if  suffix_filter(event.name):                                           
            print "Modifing:", event.pathname                                       

    def process_default(self, event):                                               
        print "Default:", event.pathname

handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch('./', mask, rec=True)

notifier.loop()


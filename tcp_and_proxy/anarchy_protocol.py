#!/usr/bin/env python

# $Id: 20130226$
# $Date: 2013-02-26 22:48:36$
# $Author: Marek Lukaszuk$

# anarchy protocol aka stateless protocol ;)

import sys
import os
import time
import struct

class anarchy():

  def __init__(self, logts=True, maxlen=1300, keepalivetime = 0.5):
    self.mpid = os.getpid()
    self.logts = logts
    self.maxlen = maxlen
    self.keepalivetime = keepalivetime
    self.seq = 0
    self.ack = 0
    self.sent = dict() # this will be used by the client to make sure it keeps track of send packets
    self.headfmt = "BBBH"
    self.headsize = struct.calcsize(self.headerfmt)

  def log(self, msg):
    # internal logging function
    try:
      txt="["+str(self.mpid)+"->"+str(self.chpid)+"] "+str(msg)
    except:
      txt="["+str(self.mpid)+"] "+str(msg)

    if self.logts == True:
      txt = time.asctime(time.localtime(time.time()))+" "+txt

    sys.stderr.write(txt+"\n")

  def dechead(self, head):
    pass

  def enchead(self,syn=0,fin=0,keepalive=0,moredata=0):
    # header:
    # flags(syn,fin,keepalive,moredata,0,0,0,0) == byte
    # seq = 1 byte
    # ack = 1 byte
    # size = 2 bytes

    return ""

  def decflags(self,flags):
    return list(bin(int(flags)).replace("0b",""))

  def encflags(self,flags):
    flags = [ str(d) for d in flags]
    return int("".join(flags),2)

  def transform(self, data):
    return data


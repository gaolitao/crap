#!/usr/bin/env python

# version: 20120114 

from scapy.all import conf,IP,TCP,sniff,send
conf.verb = 0 

from md5 import md5
from time import sleep
from socket import inet_pton
from struct import unpack,pack
from random import randint
import os
import sys

# TODO
# add logic to support subnets (IPv4/IPv6)
# add range of ports
# randomize asking

hosts = sys.argv[1]
port = int(sys.argv[2])
seen = []

# uniq seqence number generator based on some data
def seqgen(data):
  return int(str(md5(data).hexdigest()),16)%4294967296 # % max seq num

# function to check and print matching packets
def checkpkt(pkt):
  if pkt.haslayer(TCP) and pkt.getlayer(TCP).flags == 18: # 18 eq SA
    txt = pkt.payload.src+":"+str(pkt.sport)
    if pkt.getlayer(TCP).ack-1 == seqgen(txt):
      global seen
      if txt not in seen:
        print txt
        seen.append(txt)
        return False # True if you want to capture the packets 
      else:
        return False
    else:
      return False
  else:
    return False

def int2addr(data,ip6 = False):
  if ip6 == True:
    a = hex(data).lstrip("0x").zfill(32)
    return "{0}:{1}:{2}:{3}:{4}:{5}:{6}:{7}".format() # FIXME
  else:
    a = hex(data).lstrip("0x").zfill(8)
    return "{0}.{1}.{2}.{3}".format(int(a[0]+a[1],16),int(a[2]+a[3],16),int(a[4]+a[5],16),int(a[6]+a[7],16))

if __name__ == '__main__':

  ip6 = False
  maxmask = 32

  if ":" in hosts:
    ip6 = True
    maxmask = 128

  msk = maxmask 

  if "/" in hosts:
    (net,msk) = hosts.split("/")
    msk = int(msk)
  else:
    net = hosts

  if ip6 == True:
    laddr = unpack("!QQ",inet_pton(10,net)) # FIXME
    numhosts = 0xffffffffffffffffffffffffffffffff>>msk
  else:
    laddr = (unpack("!I",inet_pton(2,net)))[0]
    numhosts = 0xffffffff>>msk

  addrbeg = (laddr>>(maxmask-msk)<<(maxmask-msk))
  addrend = (addrbeg|numhosts)
   
  cpid = os.fork()
  if cpid:
    # the sending process

    sleep(1) # to make sure that the other process started listening for packets
  
    if ip6 == False:
      pkt = IP(dst = int2addr(addrbeg))/TCP(sport = 1026, dport = port)
    else:
      pkt = IPV6(dst = int2addr(addrbeg))/TCP(sport = 1026, dport = port)
    
    host = addrbeg
    
    while host < addrend:
      ip = int2addr(host)
      pkt.getlayer(IP).dst = ip 
      pkt.getlayer(TCP).seq = seqgen(ip+":"+str(port))
      send(pkt)
      host+=1

    try:
      os.wait()
    except:
      os.kill(cpid,15)

  else:
    # this is the listening and printing process
    try:
      sniff(filter = "ip and tcp", lfilter = lambda x: checkpkt(x))
    except:
      pass
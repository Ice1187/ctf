#!/usr/bin/python

from pwn import *

r = remote('2018shell.picoctf.com', 54782)

print r.recvline()
r.recvline()
r.recvline()

while 1:
  problem = r.recvline()
  print problem
  if problem.startswith("What is the most common source IP address?"):
    r.sendline('246.69.53.233')
  elif problem.startswith("How many unique destination IP addresses were targeted by the source IP address 231.205.245.44?"):
    r.sendline('1')
  elif problem.startswith("How many unique destination IP addresses were targeted by the source IP address 246.69.53.233?"):
    r.sendline('3')
  elif problem.startswith("How many unique destination IP addresses were targeted by the source IP address 251.165.34.242?"):
    r.sendline('3')
  elif problem.startswith("How many unique destination IP addresses were targeted by the source IP address 215.239.98.18?"):
    r.sendline('1')
  elif problem.startswith("What is the number of unique destination ips a file is sent, on average?"):
    r.sendline('1.40')
  print 'line: ' + r.recvline()
  print 'line: ' + r.recvline()
  print 'line: ' + r.recvline()

r.close()


"""

33d8: 48.246, 125.106
f2d2: 164.233
581d: 48.246
8aa1: 231.241, 168.19
6629: ???.???

{
    "tickets": [
        {
            "ticket_id": 0,
            "timestamp": "2016/02/08 08:45:56",
            "file_hash": "33d81fec987b8a8c",
            "src_ip": "246.69.53.233",
            "dst_ip": "48.173.183.246"
        },
        {
            "ticket_id": 1,
            "timestamp": "2017/03/05 06:01:41",
            "file_hash": "f2d2c758fe8853b5",
            "src_ip": "246.69.53.233",
            "dst_ip": "164.217.208.88"
        },
        {
            "ticket_id": 2,
            "timestamp": "2015/02/28 12:24:15",
            "file_hash": "33d81fec987b8a8c",
            "src_ip": "251.165.34.242",
            "dst_ip": "125.130.154.106"
        },
        {
            "ticket_id": 3,
            "timestamp": "2015/06/24 12:14:19",
            "file_hash": "581dc312cc8c16c6",
            "src_ip": "246.69.53.233",
            "dst_ip": "48.173.183.246"
        },
        {
            "ticket_id": 4,
            "timestamp": "2015/11/15 22:34:03",
            "file_hash": "8aa16b403ac7de3e",
            "src_ip": "215.239.98.18",
            "dst_ip": "231.12.49.241"
        },
        {
            "ticket_id": 5,
            "timestamp": "2015/02/06 15:42:17",
            "file_hash": "8aa16b403ac7de3e",
            "src_ip": "246.69.53.233",
            "dst_ip": "168.138.219.19"
        },
        {
            "ticket_id": 6,
            "timestamp": "2017/12/29 05:54:41",
            "file_hash": "8aa16b403ac7de3e",
            "src_ip": "251.165.34.242",
            "dst_ip": "168.138.219.19"
        },
        {
            "ticket_id": 7,
            "timestamp": "2017/10/10 13:11:20",
            "file_hash": "6629fde09ed2dab7",
            "src_ip": "251.165.34.242",
            "dst_ip": "187.229.175.225"
        },
        {
            "ticket_id": 8,
            "timestamp": "2015/01/26 00:01:08",
            "file_hash": "581dc312cc8c16c6",
            "src_ip": "231.205.245.44",
            "dst_ip": "48.173.183.246"
        },
        {
            "ticket_id": 9,
            "timestamp": "2017/05/07 09:51:22",
            "file_hash": "8aa16b403ac7de3e",
            "src_ip": "251.165.34.242",
            "dst_ip": "168.138.219.19"
        }
    ]
}
"""

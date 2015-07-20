#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Describing:
Backup webpage on time
python main.py -d jumptime -u weburl -o backpOutPath
"""
__author__ = 'sp'

import os
import urllib2
import datetime
import re
import chardet

jumptime = 60

inputurl = 'http://m.sohu.com/'
dirpath = '/tmp/backup/' # 待加入尾号有无/判断
now = datetime.datetime.now().strftime('%Y%m%d%H%M')
filepath = dirpath + str(now)
binUrlList = []
textUrlList = []

def creatFolder(filepath):
    '''creatFolder(filepath)

    :param filepath:
    :return:
    '''
    path = filepath.strip()
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(filepath)
    else:
        print "FileExists"
        return False

def parse(content, regrep):
    '''

    :param content:
    :param regrep:
    :return: re result
    '''
    p = re.compile(regrep, re.IGNORECASE)
    pattern = p.findall(content)
    return pattern

def scrapData(rawurl):
    '''

    :param rawurl:
    :return:webDataString
    '''
    try:
        request = urllib2.Request(rawurl)
        reponse = urllib2.urlopen(request, timeout = 60).read()
        encoding_dict = chardet.detect(reponse)
        web_encoding = encoding_dict['encoding']
        if web_encoding == 'utf-8' or web_encoding == 'UTF-8':
            pass
        else:
            reponse = reponse.decode('gbk','ignore').encode('utf-8')

    except urllib2.HTTPError,e:
        print(e.reason)
    else:
        # print chardet.detect(reponse.read())
        # 编码问题处理 待解决

        return reponse

def saveFile(data,path,method):
    f = open(path, method)
    f.write(data)
    f.close()

if __name__ == '__main__':
    creatFolder(filepath)
    htmltext = scrapData(inputurl)
    textLinkPre = r'http://.*?\.js|' \
                  r'http://.*?\.css'

    binLinkPre = r'http://.*?\.jpg|' \
                 r'http://.*?\.png|' \
                 r'http://.*?\.gif|' \
                 r'http://.*?\.ico|' \
                 r'http://.*?\.svg'

    textUrlList = parse(htmltext, textLinkPre)
    binUrlList = parse(htmltext, binLinkPre)

    saveFile(htmltext,filepath+'/index.html','w')
    # 资源链接转换为本地 待解决
    # Save textdata by textUrlList
    for t in range(len(textUrlList)):
        text = scrapData(textUrlList[t])
        namepre = r'(?<=/)[^/]*(?=[\n\r]|$)'
        name = parse(textUrlList[t], namepre)
        saveFile(text,filepath+'/'+name[0],'w')

    # Save binarydata by binUrlList
    for p in range(len(binUrlList)):
        data = scrapData(binUrlList[p])
        namepre = r'(?<=/)[^/]*(?=[\n\r]|$)'
        name = parse(binUrlList[p], namepre)
        saveFile(data, filepath+'/'+name[0],'wb')
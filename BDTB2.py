# author: Ccchivalry 2018/01/31
# using python2.7

import urllib
import urllib2
import re

class Tool:
    removeImg = re.compile('<img.*?>')
    removeAddr = re.compile('<a.*?>|</a>')
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    replaceTD = re.compile('<td>')
    replacePara = re.compile('<p.*?>')
    replaceBR = re.compile('<br>|<br/>')
    removeExtraTag = re.compile('<.*?>')
    
    def replace(self, x):
        x = re.sub(self.removeImg, '', x)
        x = re.sub(self.removeAddr, '', x)
        x = re.sub(self.replaceLine, '\n', x)
        x = re.sub(self.replaceTD, '\t', x)
        x = re.sub(self.replacePara, '\n    ', x)
        x = re.sub(self.replaceBR, '\n', x)
        x = re.sub(self.removeExtraTag, '', x)
        return x.strip()

class BDTB:
    def __init__(self, baseUrl, seeLZ, floorTag):
        print 'Initiating...'
        self.baseURL = baseUrl
        self.seeLZ = '?see_lz=' + str(seeLZ)
        self.tool = Tool()
        self.floor = 1
        self.defaultTitle = u'Baidu TieBa'
        self.floorTag = floorTag
        self.file = None
    
    def getPage(self, pageNum):
        try:
            print 'Getting Page...'
            url = self.baseURL + self.seeLZ + '&pn=' + str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            #print response.read()
            return response.read().decode('utf-8')
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print 'Connection Failed. Reason:', e.reason
                return None
        except:
            print 'Error!'
    
    def getTitle(self, page):
        pattern = re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>', re.S)
        title = re.search(pattern, page)
        print 'Getting Title...'
        if title:
            #print title.group(1).strip()
            return title.group(1).strip()
        else: 
            return None
    
    def getTotalPageNum(self, page):
        pattern = re.compile('<li class="l_reply_num.*?class="red">(.*?)</span>', re.S)
        TotalPageNum = re.search(pattern, page)
        print 'Getting Total Page Number...'
        if TotalPageNum:
            #print TotalPageNum
            return TotalPageNum.group(1).strip()
        else: 
            return None
    
    def getContent(self, page):
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>', re.S)
        items = re.findall(pattern, page)
        print 'Getting Page Content...'
        contents = []
        for item in items:
            content = '\n' + self.tool.replace(item) + '\n'
            contents.append(content.encode('utf-8'))
        return contents
    
    def setFileTitle(self, title):
        if title is not None:
            self.file = open(title + '.txt', 'w+')
        else:
            self.file = open(self.defaultTitle + '.txt', 'w+')
    
    def writeData(self, contents):
        print 'Writing Data...'
        for item in contents:
            if self.floorTag == '1':
                floorLine = '\n' + str(self.floor) + u' Floor ---------------------------------------------------------------' + '\n'
                self.file.write(floorLine)
            self.file.write(item)
            self.floor += 1
        
    def start(self):
        print 'Starting...'
        indexPage = self.getPage(1)
        pageNum = self.getTotalPageNum(indexPage)
        title = self.getTitle(indexPage)
        self.setFileTitle(title)
        if pageNum == None:
            print 'URL has outdated, please try again!'
            return
        try:
            print 'Total Page : ' + str(pageNum) + ' page'
            for i in range(1, int(pageNum)+1):
                print 'Loading the ' + str(i) + ' page'
                page = self.getPage(i)
                contents = self.getContent(page)
                self.writeData(contents)
        except IOError, e:
            print 'Error in writing file. Reason: ' + e.message
        finally:
            print 'Loading task done!'

print 'Please enter the blog number:'
baseURL = 'http://tieba.baidu.com/p/' + raw_input('http://tieba.baidu.com/p/')
seeLZ = raw_input('Whether get the authors\' contents only? Input 1 for yes, otherwise input 0:\n')
floorTag = raw_input('Whether write the floor number to files? Input 1 for yes, otherwise input 0:\n')
bdtb = BDTB(baseURL, seeLZ, floorTag)
bdtb.start()

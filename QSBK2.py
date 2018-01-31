#author: Ccchivalry 2018/01/29

import urllib
import urllib2
import re

class QSBK:
    # initializing
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/4.0(compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}
        # store the stories from website
        self.stories = []
        self.enable = False
        
    # get page html information and decode, return the decode html, or None(if connection failed)
    # pass the pageIndex value, not from the class itself
    def getPage(self, pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print 'Connection failed. Error:', e.reason
                return None
    
    # compile the objective pattern of page code, and match with the original decode html
    # store the stories in pageStories variable, and return pageStories
    def getPageItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print '页面加载失败...'
            return None
        # regular expressions for matching, withdraw the author name, story content and vote numbers into items[0], items[1], items[2]
        pattern = re.compile('<div.*?author clearfix">.*?a.*?<img.*?<a.*?<h2>(.*?)</h2>.*?<div.*?content".*?span>(.*?)</span>.*?<div class="stats.*?number">(.*?)</i>.*?', re.S)
        # re.findall (find all the substring that matches the regular expression) and return the successfully matching substring
        items = re.findall(pattern, pageCode)
        pageStories = []
        for item in items:
            pageStories.append([item[0].strip(), item[1].strip(), item[2].strip()])
        return pageStories
    
    # if self.enable is True and the self.stories lengh is less than 2, load self.pageIndex page into pageStories and increase self.pageIndex by 1, which means next time loading next page
    def loadPage(self):
        if self.enable == True:
            if len(self.stories) < 2:
                pageStories = self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex +=1
    
    # input some assigned value and then return one story at a time from pageStories, turn the enable back to False again
    def getOneStory(self, pageStories, page):
        for story in pageStories:
            # raw_input considers all input content as string type, and its return type of raw_input is string type, which enable variable input can compare with 'Q'
            # while input() requires the input content to be python expression
            input = raw_input()
            self.loadPage()
            # if input 'Q', then exit the story loading process by turing the self.enabel button to False
            if input == 'Q':
                self.enable = False
                return
            print u'第%d页\t发布人：%s\t赞：%s\n%s' % (page, story[0], story[2], story[1])
            
    # just remember to delete the already output stories from self.stories
    def start(self):
        print u'正在读取糗事百科，按回车键查看新段子，Q退出'
        self.enable = True
        self.loadPage()
        nowpage = 0
        while self.enable:
            if len(self.stories) > 0:
                pageStories = self.stories[0]
                nowpage += 1
                del self.stories[0]
                self.getOneStory(pageStories, nowpage)
    
spider = QSBK()
spider.start()

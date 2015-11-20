import scrapy
import random
import string
import urllib
import urllib2
import cookielib
import re
import json
import WeiboEncode
import WeiboSearch
from scrapy.http import Request, FormRequest
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy import log

class weiboSpider(CrawlSpider):
    
    name = "weibo"
    userName = 'deadflyy5280@sina.com'
    passWord = '882258'
    enableProxy = False
    
    serverUrl = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.11)&_=1379834957683"
    loginUrl = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.11)"
    postHeader = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0'}
    myUrl = "http://weibo.com/u/2411545895/home?wvr=5"
    
    allowed_domain = ["http://login.sina.com.cn/"]
    start_urls = ["http://login.sina.com.cn/"]#"https://class.coursera.org/patterndiscovery-001/lecture"]
    
    
    
    
        
    def start_requests(self):
        self.Login()
        self.EnableCookie(self.enableProxy)
        
        serverTime, nonce, pubkey, rsakv = self.GetServerTime()
        postData = WeiboEncode.PostEncode(self.userName, self.passWord, serverTime, nonce, pubkey, rsakv)
        print "Post data length:\n", len(postData)
        req = urllib2.Request(self.loginUrl, postData, self.postHeader)
        print "Posting request..."
        result = urllib2.urlopen(req)
        text = result.read()
        try:
            loginUrl = WeiboSearch.sRedirectData(text)
            #urllib2.urlopen(loginUrl)
            return [Request(loginUrl,meta = {'cookiejar': 1},callback = self.parse_info)]             
        except:
            print 'Login error!'
            return False
             
              
    def _log_page(self, response, filename):
        with open(filename, 'w') as f:
            f.write("%s\n%s\n%s\n" % (response.url, response.headers, response.body))                     
    
    def parse_info(self,response):
        self._log_page(response,'login_info.html')
        return [FormRequest(self.myUrl,headers = self.postHeader,\
                                          meta = {'cookiejar':response.meta['cookiejar']},\
                                          callback = self.parse_mainpage)]
    def parse_mainpage(self,response):
        self._log_page(response,'main_page.html')
    
    
    
    
    
    
    
    
    
    
    
            
    def EnableCookie(self, enableProxy):
        "Enable cookie & proxy (if needed)."
    
        cookiejar = cookielib.LWPCookieJar()
        cookie_support = urllib2.HTTPCookieProcessor(cookiejar)
        if enableProxy:
            proxy_support = urllib2.ProxyHandler({'http':'http://xxxxx.pac'})
            opener = urllib2.build_opener(proxy_support, cookie_support, urllib2.HTTPHandler)
            print "Proxy enabled"
        else:
            opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)
    
    def GetServerTime(self):
        "Get server time and nonce, which are used to encode the password"
    
        print "Getting server time and nonce..."
        serverData = urllib2.urlopen(self.serverUrl).read()
        print serverData
        try:
            serverTime, nonce, pubkey, rsakv = WeiboSearch.sServerData(serverData)
            return serverTime, nonce, pubkey, rsakv
        except:
            print 'Get server time & nonce error!'
            return None 
    
        
    
    
        
       
        
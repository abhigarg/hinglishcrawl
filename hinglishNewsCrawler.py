import os
import urllib2
from bs4 import BeautifulSoup
from threading import Thread
from  __builtin__ import any as b_any
import re

class BobbleHinglish(Thread):
    def __init__(self, lower, upper):
        Thread.__init__(self)
        self.domain = 'http://hinglish.newson.co.in/'
        self.download_path = "/media/DATA/fromUbuntu/Bobble/keyboard/hinglish_corpus/hinglishnews"
        self.opener = urllib2.build_opener()
        self.opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
        url = 'http://hinglish.newson.co.in/2015/07/13/manoranjan/pehle-dabangg-aur-ab-singham-ke-saath-main-hoon-na/600'
        self.article_url_list = [url]
        self.url_ind = 0
        self.limit = upper
        self.html = ""

        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)

    def run(self):
        count = 0
        while self.url_ind < len(self.article_url_list):
            self.download_article()
            count = count + 1
            print "TRY: ", count

    def generate_article_url(self):
        self.article_counter += 1
        return self.domain + "1.{0:06d}".format(self.article_counter), "1.{0:06d}.txt".format(self.article_counter)

    def download_article(self):
        url = self.article_url_list[self.url_ind]
        print "SEARCH : ", url
        try:
            response = self.opener.open(url)
            html = response.read()
            urls = re.findall('http[s]?:\/\/hinglish.newson.co.in(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', html)            
            print "Found new urls: ", len(urls)
            for u in set(urls):
                urlstr = u
                print "urlstr: ", urlstr                
                if u and re.search(r'\d+$', urlstr) not in None:
                    print "url: ", urlstr                     
                    if not b_any(urlstr in x for x in self.article_url_list):                    
                        self.article_url_list.add(urlstr)
                        print "added to url list: ", urlstr

            if len(self.article_url_list) > self.url_ind:
                self.url_ind = self.url_ind + 1

            soup = BeautifulSoup(html, 'html.parser')
            if soup:                
                article = soup.find("div", class_="td-post-content td-pb-padding-side")
                if article:
                    data = article.text.strip()
                    if len(data) > 0:
                        print "RECEIVED : ", data
                        fp = open(os.path.join(self.download_path, "articles.txt"), "+a")
                        fp.write(data)
                        fp.close()
        except Exception as e:
            print "EXCEPTION : ", e


if __name__ == "__main__":    
    downloader = BobbleHinglish(100, 200)
    downloader.start()
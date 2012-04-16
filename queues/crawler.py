#!/usr/bin/env python
# encoding: utf-8
"""
crawler.py

Created by  on 2012-03-17.
Copyright (c) 2012 Jesús Navarrete. All rights reserved.
"""

import urllib

def get_page(url):
    try:
        return urllib.urlopen(url).read()
    except:
        return ""

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)

def get_all_links(page):
    links = []
    while True:
        url,endpos = get_next_target(page)
        if url:
            if url[:7] == 'http://':
                links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def crawl_web_old(seed,max_pages):
    tocrawl = [seed]
    crawled = []
    count = 0
    while tocrawl and count < max_pages:
        page = tocrawl.pop()
        print '- ' + page
        if page not in crawled:
            union(tocrawl, get_all_links(get_page(page)))
            crawled.append(page)
        count = count + 1
    return crawled
    
def add_to_index(index,keyword,url):
    for entry in index:
        if entry[0] == keyword:
            entry[1].append(url)
            return
    index.append([keyword, [url]])

def add_page_to_index(index, url, content):
    words = content.split()
    for w in words:
        add_to_index(index, w, url)

def lookup(index, keyword):
    for node in index:
        if node[0] == keyword:
            return node[1]
    return []

def crawl_web(seed):
    tocrawl = [seed]
    crawled = []
    index = []
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            print '- ' + page
            content = get_page(page)
            add_page_to_index(index, page, content)
            union(tocrawl, get_all_links(content))
            crawled.append(page)
    return index
    
def main(seed):
    return crawl_web(seed)


if __name__ == '__main__':
	main('http://www.infoq.com')


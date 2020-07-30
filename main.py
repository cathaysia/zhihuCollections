#!/usr/bin/python3

import bs4, time
from urllib.parse import urljoin
from selenium import webdriver

# 收藏夹的地址
BASE = r'https://www.zhihu.com/people/hello-77-60-98/collections'

# 将结果导出为 Firefox html书签
BookMarks = '''
<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
     It will be read and overwritten.
     DO NOT EDIT! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>书签菜单</H1>
<DL><p>
    <DT><H3 ADD_DATE="1595736880" LAST_MODIFIED="1596072070" PERSONAL_TOOLBAR_FOLDER="true">书签工具栏</H3>
    <DL><p>
        <DT><H3 ADD_DATE="1555768086" LAST_MODIFIED="1596072070">知乎收藏夹</H3>
        <DL><p>
'''

ITEM = '''
            <DT><A HREF="{}">{}</A>

'''

browser = webdriver.Firefox()

def getContent(url:str) -> str:
    # 获取 url 对应的网页内容
    browser.get(url)
    for i in range(1, 5):
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(1)
    return browser.page_source

colList = {} # 保存知乎收藏夹内的所有结果

def getCollections() -> [str]:
    # 获取收藏夹的url
    colections = getContent(BASE)
    soup = bs4.BeautifulSoup(colections, 'lxml')
    s = soup.select(r'''a[href^="/collection"]''')
    urllist = []
    for a in s:
        urllist.append(urljoin(BASE, a['href']))
    print("你一共有" + str(len(urllist)) + "个搜藏夹")
    return urllist

def getLists(page:str) -> {str:str}:
    # 解析收藏夹页面内容
    bs = bs4.BeautifulSoup(page, 'lxml')
    contentList = bs.select('h2.ContentItem-title')
    for node in contentList:
        title = node.a.get_text()
        url = node.a['href']
        colList[title] = urljoin(BASE, url)
    return colList

def getPageCounter(page:str) -> int:
    bs = bs4.BeautifulSoup(page, 'lxml')
    # 获取收藏夹的名字
    name = bs.select("div.CollectionDetailPageHeader-title")[0].get_text()
    print("你的" + name + "收藏夹一共有")
    # 获取收藏夹一共有几页
    result = bs.select("div.Pagination")
    if(len(result) == 0):
        print("1页")
        return 1
    totle_list = result[0].select('button')
    print(str(len(totle_list) - 1) + "页")
    return len(totle_list) - 1

if __name__ == "__main__":
    #获取收藏夹的url
    urllist = getCollections()
    for url in urllist:
        print(url)
        # 打开收藏夹网页
        page = getContent(url)
        # with open('main.html', mode="r") as f:
        #     page = f.read()
        for s in range(0, getPageCounter(page)):
            totle_url = url + '?page=' + str(s+1)
            print(totle_url)
            col_page = getContent(totle_url)
            getLists(col_page)
    # 现在，所有的收藏夹内的url被储存到 colList 内
    for key in colList.keys():
        url = colList[key]
        book_mark = ITEM.format(url, key)
        print(book_mark)
        BookMarks += book_mark
    BookMarks+='''
            </DL><p>
    </DL><p>
</DL>
    '''
    with open('bookMarks.html', 'w+') as f:
        f.write(BookMarks)
        f.close()







'''
<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
     It will be read and overwritten.
     DO NOT EDIT! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>书签菜单</H1>
<DL><p>
    <DT><H3 ADD_DATE="1595736880" LAST_MODIFIED="1596072070" PERSONAL_TOOLBAR_FOLDER="true">书签工具栏</H3>
    <DL><p>
        <DT><H3 ADD_DATE="1555768086" LAST_MODIFIED="1596072070">知乎收藏夹</H3>
        <DL><p>
            <DT><A HREF="https://www.cnblogs.com/kongzhagen/p/6472746.html">beautifulsoup之CSS选择器 - 孔扎根 - 博客园</A>
        </DL><p>
    </DL><p>
</DL>
'''

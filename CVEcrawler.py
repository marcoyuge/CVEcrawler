import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

excel_name = "vulnerabilities.xlsx"
wb = Workbook()
ws1 = wb.active
ws1.title = 'bugs'
baseurl = 'http://cve.scap.org.cn'


def gethtml(i):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    url = 'http://cve.scap.org.cn/vulns/%d' % i
    res = requests.get(url, headers=header).content
    return res #返回第i页的网页内容


def getbugdes(url):
    url = baseurl + url
    res = requests.get(url).content
    soup = BeautifulSoup(res, 'html.parser')
    div = soup.find('div', attrs={'class': 'row bug_article font14 mrg15B pad15B'})
    p = div.find('p', attrs={'class': 'pad30T pad30B mrg0B'})
    return p.text.strip()  # 返回bug的描述文字


def getconlist(res):
    soup = BeautifulSoup(res, 'html.parser')
    vullist = soup.find('div', attrs={'class': 'container bugs padb bugs_list'}).find('table')
    bugnames = vullist.find_all('a')
    nameresultslist = []
    deslist = []
    for bugname in bugnames:#根据获取到的bug列表进一步获取bug名和bug描述
        nameresultslist.append(bugname.text.strip())
        deslist.append(getbugdes(bugname['href']))
    return nameresultslist, deslist #返回每一页的bug名和bug描述


def saveasexcel(namelist, deslist, i):
    for name in namelist:
        loc = 'A{}'.format(namelist.index(name) + 1 + i * 10)  # 第i页开始的数据记录在excel表的第i*10行
        ws1[loc] = name
    for des in deslist:
        loc = 'B{}'.format(deslist.index(des) + 1 + i * 10)
        ws1[loc] = des
    wb.save(filename=excel_name)


def run(pagenum):#根据输入的页数，循环对每一页进行操作
    for i in range(pagenum):
        html = gethtml(i + 1)
        namelist, deslist = getconlist(html)
        saveasexcel(namelist, deslist, i)


if __name__ == '__main__':
    run(5)  # 想爬前多少页就写多少

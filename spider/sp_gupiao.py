import requests
from bs4 import BeautifulSoup
import traceback
import re

def getHTMLText(url,code='utf-8'):
    try:
        r=requests.get(url)
        r.raise_for_status()
        r.encoding=code
        return r.text
    except:
        return ""
    print('获取url')
def getStockList(lst,stockURL):
    html=getHTMLText(stockURL,'GB2312')
    soup=BeautifulSoup(html,'html.parser')
    a=soup.find_all('a')
    for i in a:
        try:
            href=i.attrs['href']
            lst.append(re.findall(r"[s][hz]\d{6}",href)[0])
        except:
            continue
    print("获取列表")

def getStockInfo(lst,stockURL,fpath):
    count=0
    for stock in lst:
        url=stockURL+stock#+".html"
        html=getHTMLText(url)
        try:
            if html=="":
                continue
            infoDict={}
            soup=BeautifulSoup(html,'html.parser')
            stockInfo=soup.find('div',attrs={'class':'stock_header_wrap'})

            name=stockInfo.find_all(attrs='h3')[0]
            infoDict.update({'股票':name.text.split()[0]})

            keyList=stockInfo.find_all('span')
            valueList=stockInfo.find_all('b')
            for i in range(len(keyList)):
                key=keyList[i].text
                val=valueList[i].text
                infoDict[key]=val

            with open(fpath,'a',encoding='utf-8') as f:
                f.write(str(infoDict)+'\n')
                count=count+1
                print('\r当前速度：{:.2f}%'.format(count*100)/len(lst),end='')
        except:
            count=count+1
            print('\r当前速度：{:.2f}%'.format(count*100)/len(lst),end='')

            traceback.print_exc()
            continue
    print("开始获取信息")
def main():
    stock_list_url='http://quote.eastmoney.com/stocklist.html'
    stock_info_url='https://www.aigupiao.com/Quote/stock_market?code='
    output_file='/home/stock.txt'
    slist=[]
    getStockList(slist,stock_list_url)
    getStockInfo(slist,stock_info_url,output_file)

main()
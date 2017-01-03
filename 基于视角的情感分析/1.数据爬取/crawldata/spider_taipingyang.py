# -*- coding: UTF-8 -*-
import urllib
import urllib2
import json
from lxml import etree
import json
import datetime
def parse(response):
    pass

def send_request(url, data=None):
    req = urllib2.Request(url,data)
    response = urllib2.urlopen(req)
    context = response.read()
    context = unicode(context, 'gbk')
    return context


def parse_js(url):
    context = send_request(url)
    context = context.split("='")[1].strip("';")
    selector = etree.HTML(context)
    brands = selector.xpath('//a[contains(@id, "brand")]/big/text()')  # 返回为一列表
    products = selector.xpath('//a/big/text()')  # 返回为一列表

    brands_products = {}
    cur_brand = brands[0]
    i = 0
    for each in products:
        if each == brands[i]:
            brands_products[brands[i]] = []
            cur_brand = brands[i]
            if i < brands.__len__() - 1:
                i += 1
        else:
            brands_products[cur_brand].append(each)

    print "brands_products:"
    print brands_products
    return brands_products
    # return brands, products

def get_one_js():
    data = {}
    data['name'] = 'WHY'
    data['location'] = 'SDU'
    data['language'] = 'Python'
    url_values = urllib.urlencode(data)
    url = 'http://price.pcauto.com.cn/index/js/5_5/treedata-cn-1.js'
    selector = etree.HTML(url)  # 将源码转化为能被XPath匹配的格式
    print selector
    res = selector.xpath('//a[contains(@id, "product")]/big/text()')  # 返回为一列表
    # print context
    for each in res:
        print each

def spider_taipingyang():
    selector = etree.HTML(html())  # 将源码转化为能被XPath匹配的格式
    # print selector
    car_types = selector.xpath('//a[contains(@id, "pictext")]/@title')  # 返回为一列表
    id_nums = selector.xpath('//a[contains(@id, "pictext")]/@id')  # 返回为一列表
    for each in car_types:
        print each

    res = {}
    for i in range(id_nums.__len__()):
        url = "http://price.pcauto.com.cn/index/js/5_5/treedata-cn-" + id_nums[i].split("a_")[1] + ".js"
        res[car_types[i]] = parse_js(url)

    with open('car_taipingyang1.json' + datetime.timedelta, 'w') as f:
        f.write(json.dumps(res))


if __name__=="__main__":
    # print ord('A')
    cars_json = {}
    brands = {}
    for i in xrange(26):
        url = 'http://www.autohome.com.cn/grade/carhtml/' + chr(i + ord('A')) +'.html'
        if chr(i + ord('A')) in ['E' , 'I' , 'U' , 'V']:
            continue
        print  url
        context = send_request(url)
        # print context
        selector = etree.HTML(context)
        j = 1
        company = {}
        products = {}
        # print  context
        brands_company_products={}
        while(True):
            brand_tmp = selector.xpath("//html/body/dl[%s]/dt/div/a/text()" % j)  # 返回为一列表
            if brand_tmp == []:
                break

            company[j] = {}
            company_tmp = selector.xpath("//html/body/dl[%s]/dd/div[@class='h3-tit'][1]" % j)[0]
            company_name = company_tmp.xpath(".//text()")[0]
            while(True):
                products = company_tmp.xpath(".//following-sibling::ul[1]/li[@id]/h4/a/text()")
                products_tmp = company_tmp.xpath(".//following-sibling::ul[1]")[0]
                company[j][company_name] = products
                company_tmp = products_tmp.xpath(".//following-sibling::div[@class='h3-tit'][1]")
                if company_tmp == []:
                    break
                else:
                    company_tmp = products_tmp.xpath(".//following-sibling::div[@class='h3-tit'][1]")[0]

                company_name = company_tmp.xpath(".//text()")[0]

            brands[brand_tmp[0]] = company[j]  # 返回为一列表
            print brands
            j += 1

    with open('car_qichezhijia.json', 'w') as f:
        f.write(json.dumps(brands))




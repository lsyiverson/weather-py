#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding=utf-8
import urllib2
from lxml import etree
from datetime import datetime, timedelta
import re
from utils.fileutils import mkdir, touch ,append, rmtree
from openpyxl import Workbook

rmtree('./aqiresult')
pattern = re.compile('\s+')

site = 'http://tianqihoubao.com'
homePage = urllib2.urlopen(site + '/aqi/').read().decode('gbk').encode('utf8').replace('<wbr>', '')

homePageHtml = etree.HTML(homePage, parser=etree.HTMLParser(encoding='utf8'))

provinceElementXPath = homePageHtml.xpath('//div[@id="content"]/div[@class="citychk"]/dl')

workbook = Workbook()
cnAQIWorksheet = workbook.active
cnAQIWorksheet.title = 'China City AQI'
cnAQIWorksheet.append(['省份', '城市', '日期', '质量等级', 'AQI指数', '当天AQI排名', 'PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3'])

for provinceIndex, provinceElmTree in enumerate(provinceElementXPath):
#     provinceIndex = 2
#     provinceElmTree = provinceElementXPath[provinceIndex]
    provinceName = provinceElmTree.find('dt/b').text
    provincePath = './aqiresult/' + provinceName
    mkdir(provincePath)

    for cityIndex, cityElm in enumerate(provinceElmTree.findall('dd/a')):
        # cityIndex = 0
        # cityElm = provinceElmTree.findall('dd/a')[cityIndex]
        if (provinceIndex == 0 and cityIndex > 3):
            break

        cityName = cityElm.text
        filepath = provincePath + '/' + cityName.strip() + '.txt'
        touch(filepath)

        cityPre = re.sub(pattern, '', cityElm.attrib['href'])[:-5]
        startMonth = '201501'
        for i in range(24):
            # i=0
            startMonth = datetime.strptime('201501', '%Y%m')
            month = startMonth.replace(year=startMonth.year+i/12, month=startMonth.month+i%12)
            monthstr = month.strftime('%Y%m')

            cityMonthAqiUrl = site + cityPre + '-' + monthstr + '.html'
            cityMonthAqiPage = urllib2.urlopen(cityMonthAqiUrl).read().decode('gbk').encode('utf8')
            cityMonthAqiPageHtml = etree.HTML(cityMonthAqiPage, parser=etree.HTMLParser(encoding='utf8'))

            cityMonthAqiContentXPath = cityMonthAqiPageHtml.xpath('//div[@class="api_month_list"]/table[@class="b"]/tr')
            monthlyData = ''
            for dailyAqiElmTree in cityMonthAqiContentXPath[1:]:
                date = re.sub(pattern, '', dailyAqiElmTree.findall('td')[0].text)
                level = re.sub(pattern, '', dailyAqiElmTree.findall('td')[1].text)
                aqi = re.sub(pattern, '', dailyAqiElmTree.findall('td')[2].text)
                rank = re.sub(pattern, '', dailyAqiElmTree.findall('td')[3].text)
                pm25 = re.sub(pattern, '', dailyAqiElmTree.findall('td')[4].text)
                pm10 = re.sub(pattern, '', dailyAqiElmTree.findall('td')[5].text)
                no2 = re.sub(pattern, '', dailyAqiElmTree.findall('td')[6].text)
                so2 = re.sub(pattern, '', dailyAqiElmTree.findall('td')[7].text)
                co = re.sub(pattern, '', dailyAqiElmTree.findall('td')[8].text)
                o3 = re.sub(pattern, '', dailyAqiElmTree.findall('td')[9].text)

                cnAQIWorksheet.append([provinceName, cityName, date, level, aqi, rank, pm25, pm10, no2, so2, co, o3])

                format = '%s %s %s %s %s %s %s %s %s %s'
                values = (date, level, aqi, rank, pm25, pm10, no2, so2, co, o3)
                dailyAqiData = format % values
                monthlyData += dailyAqiData + '\n'
            append(filepath, monthlyData)
            print provinceName + cityName + monthstr + u' 下载成功'
workbook.save('./aqiresult/aqi.xlsx')
print u'导出Excel成功'






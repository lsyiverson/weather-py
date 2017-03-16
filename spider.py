#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding=utf-8
import urllib2
from lxml import etree
from datetime import datetime, timedelta
import re
from utils.fileutils import mkdir, touch ,append, rmtree
from openpyxl import Workbook

rmtree('./result')
pattern = re.compile('\s+')

site = 'http://tianqihoubao.com'
homePage = urllib2.urlopen(site + '/lishi/').read().decode('gbk').encode('utf8').replace('<wbr>', '')

homePageHtml = etree.HTML(homePage, parser=etree.HTMLParser(encoding='utf8'))

provinceElementXPath = homePageHtml.xpath('//div[@id="content"]/div[@class="citychk"]/dl')

workbook = Workbook()
cnWeatherWorksheet = workbook.active
cnWeatherWorksheet.title = 'China Weather'
cnWeatherWorksheet.append(['省份', '城市', '日期', '日间天气', '夜间天气', '最高温度', '最低温度', '日间风力风向', '夜间风力风向'])

for provinceElmTree in provinceElementXPath:
    # provinceElmTree = provinceElementXPath[2]
    provinceName = provinceElmTree.find('dt/a/b').text
    provincePath = './result/' + provinceName
    mkdir(provincePath)

    for cityElm in provinceElmTree.findall('dd/a'):
        # cityElm = provinceElmTree.findall('dd/a')[0]
        cityName = cityElm.text
        filepath = provincePath + '/' + cityName.strip() + '.txt'
        touch(filepath)

        cityPre = cityElm.attrib['href'][:-5]
        startMonth = '201601'
        for i in range(12):
            # i=0
            startMonth = datetime.strptime('201601', '%Y%m')
            month = startMonth.replace(year=startMonth.year, month=startMonth.month+i)
            monthstr = month.strftime('%Y%m')

            cityMonthWeatherUrl = site + cityPre + '/month/' + monthstr + '.html'
            cityMonthWeatherPage = urllib2.urlopen(cityMonthWeatherUrl).read().decode('gbk').encode('utf8')
            cityMonthWeatherPageHtml = etree.HTML(cityMonthWeatherPage, parser=etree.HTMLParser(encoding='utf8'))

            cityMonthWeatherContentXPath = cityMonthWeatherPageHtml.xpath('//div[@id="content"]/table[@class="b"]/tr')
            monthlyData = ''
            for dailyWeatherElmTree in cityMonthWeatherContentXPath[1:]:
                date = re.sub(pattern, '', dailyWeatherElmTree.findall('td')[0].find('a').text)

                weather = re.sub(pattern, '', dailyWeatherElmTree.findall('td')[1].text)
                weatherSet = weather.split('/')
                dayWeather = weatherSet[0]
                nightWeather = weatherSet[1]

                temperature = re.sub(pattern, '', dailyWeatherElmTree.findall('td')[2].text)
                tempSet = temperature.split('/')
                highestTemp = tempSet[0]
                lowestTemp = tempSet[1]

                wind = re.sub(pattern, '', dailyWeatherElmTree.findall('td')[3].text)
                windSet = wind.split('/')
                dayWind = windSet[0]
                nightWind = windSet[1]

                cnWeatherWorksheet.append([provinceName, cityName, date, dayWeather, nightWeather, highestTemp, lowestTemp, dayWind, nightWind])

                format = '%s %s %s %s'
                values = (date, weather, temperature, wind)
                dailyWeatherData = format % values
                monthlyData += dailyWeatherData + '\n'
            append(filepath, monthlyData)
            print provinceName + cityName + monthstr + u' 下载成功'
workbook.save('./result/weather.xlsx')
print u'导出Excel成功'






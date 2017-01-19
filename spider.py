# encoding=utf-8
import urllib2
from lxml import etree
from datetime import datetime, timedelta
import re
from utils.fileutils import mkdir, touch ,append, rmtree

rmtree('./result')
pattern = re.compile('\s+')

site = 'http://tianqihoubao.com'
homePage = urllib2.urlopen(site + '/lishi/').read().decode('gbk').encode('utf8')

homePageHtml = etree.HTML(homePage, parser=etree.HTMLParser(encoding='utf8'))

provinceElementXPath = homePageHtml.xpath('//div[@id="content"]/div[@class="citychk"]/dl')

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
                temperature = re.sub(pattern, '', dailyWeatherElmTree.findall('td')[2].text)
                wind = re.sub(pattern, '', dailyWeatherElmTree.findall('td')[3].text)

                format = '%s %s %s %s'
                values = (date, weather, temperature, wind)
                dailyWeatherData = format % values
                monthlyData += dailyWeatherData + '\n'
            append(filepath, monthlyData)
            print provinceName + cityName + monthstr






#! /usr/bin/python
# -*- coding: utf-8 -*-
# File Name		: crl_now.py
# Author			 : 
# Creation Date: 2014 06 06 02:22

from timeweather import *
import datetime
from urllib import urlopen

# Fetch source HTML of specified page
# Return: Page source, or exit if exception.
def get_page(url):
        try:
                page = urlopen(url).read()
                return page

        except Exception, err:
                print "Fail to get the page: " + str(err)
                exit()

# Find all tag ... endtag
# Return: A list with text in specified tag
def find_tag_text(instr, tag, endtag):
        resultList = []
        curPos = 0

        while True:
                curPos = instr.find(tag, curPos)
                if curPos == -1:
                        break
                endPos = instr.find(endtag, curPos)
                if endPos != -1:
                        resultList.append(instr[curPos + len(tag):endPos])
                else:
                        resultList.append(instr[curPos + len(tag):len(instr) - 1])
                        break
                curPos = endPos + 1
        
        return resultList

# Remove all tags (Reg: <(\w+)>)
# Same as ".text" in BeautifulSoup4
# Return: the string without any tag
def remove_all_tag(instr):
        s = ""
        fetch = True

        for ch in instr:
                if ch == '<' or ch == '>':
                        fetch = not fetch
                if fetch and ch != '>' and ch != ' ':
                        s += ch
        
        return s

# Dump now weather into a binary file by using pickle.
# If there has a existed file, then load and union with existed and new one.
def record_now_weather(thisWeather, filePath):
        try: # Load the old table if existed.
                # "/curr/cody/Application/crlWeather/record_now.pkl"
                f = open(filePath, "rb")
                from pickle import load
                table = load(f)
                f.close()
                print "Record loading successed, load " + str(len(table)) + " data."
                found = False
                for e in table:
                        if e == thisWeather:
                                found = True
                                break
                if not found:
                        table.append(thisWeather)
                from operator import attrgetter
                table = sorted(table, key=attrgetter("thisDate", "thisTime"))
         
        except Exception, err: # Or create a new one.
                print "Record not found. Create a new one."
                table = [thisWeather]
                pass

        try: # Write the new table into a binary file.
                f = open(filePath, "wb")
                from pickle import dump
                dump(table, f)
                f.close()

        except Exception, err:
                print "Fail to record table: " + str(err)

        # Display the final table.
        for e in table:
                print e
                
# Fetch "number" (including float numbers).
# Return: the number in string type
def fetch_num(instr):
        nstr = ""
        for ch in instr:
                if not ch.isdigit() and ch != '.':
                        break
                nstr += ch
        return nstr

# Fetch weather data from page source.
# Return: A TIME_WEATHER with all filled data.
def fetch_now_weather(page_src):
        
        thisWeather = TIME_WEATHER()	
        dataArea = find_tag_text(page_src, '<tr class="RecreationArea-box-td-high">', "</tr>")
        attrList = ["thisTemp", "thisMoisture", "thisVol"]
        attrPtr = 0
        for d in find_tag_text(dataArea[0], "<td>", "</td>"):
                if attrPtr > 2:
                        break
                if str(d).find("<br>") != -1:
                        today = str(datetime.datetime.now(GMT8()))
                        thisWeather.thisDate = today[:today.find(' ')]
                        fetchTime = remove_all_tag(find_tag_text(d, "<br>", "</br>")[0])
                        thisWeather.thisTime = int(fetchTime[:fetchTime.find(":")])
                else:
                        value = float(fetch_num(str(remove_all_tag(d))))
                        exec("thisWeather." + attrList[attrPtr] + " = value")
                        attrPtr += 1

        return thisWeather

if __name__ == "__main__":
        from time import ctime
        from time import time
        import sys

        startTime = time()
        print "Program start at " + ctime()
        try:
                filePath = str(sys.argv[1])
        except Exception, err:
                print "Fail to get the path of record file: " + str(err)	
        page_src = get_page("http://www.cwb.gov.tw/V7/forecast/town368/GT/6300200.htm")

        print "Fetching data..."
        thisWeather = fetch_now_weather(page_src)
        record_now_weather(thisWeather, filePath)
        print "Done. Execution time: " + str(time() - startTime)


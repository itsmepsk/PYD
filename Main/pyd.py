#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#######################################################################################
#                        Python Youtube Downloader (PYD) v 1.0                        #
#                                                                                     #
#                        Author - Prathamesh Kakade                                   #
#                        https://github.com/itsmepsk                                  #
#                                                                                     #
#           PYD is utility written in python 2.7 to download Youtube videos.          #
#                                                                                     #
#           Features:                                                                 #
#           ->Displays Download progress.                                             #
#           ->Select any quality to Download with filesize.                           #
#           ->Manually enter File name.                                               #
#           ->Manually enter Download path.                                           #
#                                                                                     #
#                                                                                     #
#           Limitations:                                                              #
#           ->Cannot Download videos with NON-ASCII characters in video title.        #
#           ->Does not support Pause and Resume.                                      #
#           ->No Proxy Support.                                                       #
#                                                                                     #
#                                                                                     #
#           Requirements:                                                             #
#           The following requirements should fullfilled for using PYD.               #
#           ->Installation of PYTHON 2.7 .                                            #
#           ->BeautifulSoup library MUST be installed.                                #
#           ->Mechanize library MUST be installed.                                    #
#           ->Urllib library MUST be installed.                                       #
#                                                                                     #
#                                                                                     #
#           Instructions:                                                             #
#           1.Run the file in Command Prompt/Powershell/Terminal as                   #
#               " python pyd.py " from the directory which has this file.             #
#           2.Enter/Paste the Youtube video URL.                                      #
#           3.Select the quality to download.                                         #
#           4.Enter the PATH where the file is to be Downloaded.                      #
#           5.Enter the name of the file to be saved.                                 #
#           6.Type CTRL+Z any time to cancel.(Before download starts.)                #
#           7.Sit back and watch the Download progress ;) .                           #
#                                                                                     #
#                                                                                     #
#           WARNING:                                                                  #
#           Downloading Youtube videos is against Youtube's policy.                   #
#           Download at your own risk.I am not responsible.                           #
#                                                                                     #
#######################################################################################
'''

import BeautifulSoup
import mechanize
import os
import re
import sys
import urllib

from BeautifulSoup import BeautifulSoup
from mechanize import Browser

br = mechanize.Browser()
br.set_handle_robots(False)

##            Function to display file size

def fileSize(link):
    fil_e = urllib.urlopen(link)
    meta = fil_e.info()
    return  round(float(meta.getheaders("Content-Length")[0])/(1024*1024),2)


##            Function to display download progress

def dlProgress(count, blockSize, totalSize):
    sys.stdout.write("Downloading Video ....... ")
    percent = int(count*blockSize*100/totalSize)
    sys.stdout.write("%2d%%" % percent)
    for i in range(0,29):
        sys.stdout.write("\b")
    sys.stdout.flush()



yurl = raw_input("Enter Youtube video link : ")
url = "http://www.save-video.com/download.php?url="
url += urllib.quote_plus(yurl)



##            Fetch title of the video.

response = br.open(yurl)
html = response.read()
soup = BeautifulSoup(html)
title = soup.title.string
    
##            Crawl to extract links

response = br.open(url)
html = response.read()
soup = BeautifulSoup(html)



print "\n"

for i in range(0,len(title)+12):
    sys.stdout.write("*")
    
sys.stdout.write("\n")

print "*     " + title + "     *"

for i in range(0,len(title)+12):
    sys.stdout.write("*")
    
print "\n"



link = soup.findAll('a')

stack = list()
for each in link:
    check = each.contents[0]
    mp4 = "MP4"
    web = "WEB"
    flv = "FLV"
    tgp = "3GP"

    if( (mp4 in check) | (web in check) | (flv in check) | (tgp in check) ):
        stack.append(each)
    else:
        link.remove(each)

        
invalid = 1

while invalid == 1:
    print "*********************************"
    print "*     Available qualities :     *"
    print "*********************************"
    for i in range(0,len(stack)):
        string = "-> Enter "
        string += str(i+1);
        string += " for "
        string += stack[i].contents[0]
        var = urllib.unquote_plus(stack[i].get('href').split('generate.php?url=')[1])
        string += "      "
        string += str(fileSize(var))
        string += "MB"
        print string
    sys.stdout.write("\n")
      
    choice = input('Enter your choice : ');
    sys.stdout.write("\n")
    if( (choice < 1) | (choice > len(stack)) ):
        print "Invalid Input"
        invalid = 1
    else:
        invalid = 0
        url = stack[choice-1].get('href')
        url = url.split('generate.php?url=')[1]
        url = urllib.unquote_plus(url)
        sys.stdout.write("\n")
        path = raw_input("Enter the path to save the file.(End the path with trailing slash) : ")
        sys.stdout.write("\n")
        name = raw_input("Enter the name as to be saved.(Without extension) : ")
        sys.stdout.write("\n")
        extension = stack[choice-1].contents[0].split('(')[0]

        title = urllib.quote(title)
        fil = path
        fil += name
        fil += "."
        fil += extension

        print fil
        sys.stdout.write("\n")
        
        if urllib.urlretrieve(url, fil, reporthook=dlProgress ) :
            print "\n\n\nDownload Completed.\n"
            for i in range(0,120):
                sys.stdout.write("-")
            sys.stdout.write("\n\n\n")

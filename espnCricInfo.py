#!/usr/bin/python
import requests as rq
import notify2 as nt
import xml.etree.ElementTree as ET
import csv

#------------CONSTANTS------------#
icon="/home/nikmul19/Desktop/espn.png"
csvFileName="/home/nikmul19/Desktop/data.csv"
cricUrl="http://static.cricinfo.com/rss/livescores.xml"
fileName="/home/nikmul19/Desktop/xmlTest.xml"
heading=["item","link"]
teams=["India","South Africa","West Indies","England","New Zealand","Australia","Sri Lanka","Zimbabwe","Bangladesh"]
#-------------FUNCTIONS-----------#
def parseXml(file):
    xmlFile=open(file,"wb")
    resCode=rq.get(cricUrl)
    xmlFile.write((resCode.content))

def fetchScores(fileName):
    tree=ET.parse(fileName) 
    root=tree.getroot()
    feedList=[]
    flag={"India":-1,"South Africa":-1,"West Indies":-1,"England":-1,"New Zealand":-1,"Australia":-1,"Sri Lanka":-1,"Zimbabwe":-1,"Bangladesh":-1}
    for child in root.findall("./channel/item"):
        feedDict={}
        for team in teams:
            if team in child[0].text and (flag[team]==-1) :
                res=False
                match=child[0].text
                v1,v2=match.split(" v ")
                l=list(map(str,v1.split()))
                ll=list(map(str,v2.split()))
                len1=len(l)
                len2=len(ll)
                if(len1>=3):
                    for vals in range(10):
                        if l[2][0]==str(vals):
                            flag[" ".join(l[0:2]) ]=1
                            res=True
                            break
                if(len2>=3):
                    for vals in range(10):
                        if ll[2][0]==str(vals):
                            flag[" ".join(ll[0:2]) ]=1
                            res=True
                            break
                if(len1==2 or len1==1 or len2==2 or len2==1):
                    if(l[0] in teams ):
                        flag[team]=1
                        res=True
                    if( " ".join(l[0:2]) in teams ):
                        flag[" ".join(l[0:2])]=1
                        res=True
                    if ll[0] in teams:
                        flag[ll[0]]=1
                        res=True
                    if  " ".join(ll[0:2]) in teams:
                        flag[" ".join(ll[0:2])]=1
                        res=True
                if res==True:
                    feedDict["item"]=child[0].text
                    feedDict["link"]=child.find("guid").text
                    feedList.append(feedDict)

#----------------remove repeating Matches--------------------#
    Links={}
    for i in feedList:
        link=i["link"].split(".html")[0].split("/")[6]
        if(Links.get(link,0)==0):
           Links[link]=1
        else:
            feedList.remove(i)
    return feedList
#------------------------------------------------------------#
def writeCsv(csvFileName,feedList):
    with open(csvFileName,"w") as csvfile:
        csvObject=csv.DictWriter(csvfile,fieldnames=heading)
        csvObject.writeheader()
        csvObject.writerows(feedList)

def showNotification(csvFileName):
    with open(csvFileName,"r") as csvfile:
        reader=csv.DictReader(csvfile)
        fields=reader.fieldnames
        for row in reader:
            nt.init("cricket scores")
            n=nt.Notification(None,"live scores",icon=icon)
            n.set_urgency(nt.URGENCY_CRITICAL)
            n.set_timeout(1000)
            n.update(row[fields[0]],row[fields[1]])
            n.show()
#-----------------Main Function----------------------#

def main():    
    parseXml(fileName)
    feed=fetchScores(fileName)
    writeCsv(csvFileName,feed)
    showNotification(csvFileName)
if __name__=="__main__":
    main()


import requests
import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pydub
import urllib

baseURl = "https://www.ifaa.de/shop/ifaa-online/classes/"
baseCourseUrl = "https://www.ifaa.de/shop/ifaa-online/classes/index/?course_id="
courseIds = ["9", "12", "11", "13", "10", "8"]
driver = webdriver.Chrome('chromedriver')

def getCourseLink():
    idCount = len(courseIds)
    cId = 0
    cPlace = 0

    courseIndex = 0
    videoIndex = 0
    while idCount != cPlace:
        print("now course number " + str(courseIndex))
        cId = courseIds[cPlace]
        url = baseCourseUrl + cId;
        getVideoSidesLink(url, videoIndex,courseIndex)
        cPlace += 1
        courseIndex += 1

def getVideoSidesLink(courUrl,vIndex,cIndex):
    driver.get(courUrl)
    time.sleep(2)
    print("now in " + driver.current_url)
    frames = driver.find_elements_by_class_name("concept-list")
    print("found " + str(len(frames)) + " frames")
    children_by_xpath = frames[len(frames)-1].find_elements_by_xpath("./li/a")
    print("with " + str(len(children_by_xpath)) + " childs")
    links = []
    for st in children_by_xpath:
        links.append(st.get_attribute("href"))
    print("got " + str(len(links)) + " links")
    for st in links:
        GetVideoLink(st,vIndex,cIndex)
        vIndex += 1


def GetVideoLink(sideUrl, videoCount, courseCount):
    driver.get(sideUrl)
    time.sleep(2)
    print("now in " + driver.current_url)
    frames = driver.find_element_by_id("ifaa-video-play-main")
    src = frames.get_attribute("src")
    print("try downloading from " + src)
    downloadVideo(src,videoCount,courseCount)




def downloadVideo(url, videoCount, courseCount):
    r = requests.get(url, allow_redirects=True)
    filename = "videos/video-" + str(courseCount) + "_" + str(videoCount) + ".mp4"
    print("Started downloading of " + filename)
    open(filename, 'wb').write(r.content)
    print("finish with video download")
    driver.back()
    time.sleep(2)


driver.get(baseURl);
getCourseLink()
print("finish")




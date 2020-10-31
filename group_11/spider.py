import urllib3

urllib3.disable_warnings()
import os
import time
from selenium import webdriver  # 从selenium导入webdriver


rootPath = 'G:/成考视频/专升本高等数学二/'
startDiv = 0  # 起始div
url = 'https://biz.cli.im/sc/FI1307188?type=biz#!/' # 地址


driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
# driver.get('https://www.baidu.com') # 获取百度页面
# inputElement = driver.find_element_by_id('kw') #获取输入框
# searchButton = driver.find_element_by_id('su') #获取搜索按钮
#
# inputElement.send_keys("Python") #输入框输入"Python"
# searchButton.click() #搜索
# chrome_options = webdriver.ChromeOptions()
# prefs = {'profile.default_content_settings.popups': 1, 'download.default_directory': rootPath}
# chrome_options.add_experimental_option('prefs', prefs)
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get(url)
list = driver.find_elements_by_class_name('weui-cell_nav_p')
length = len(list)
for i in range(startDiv, length, 2):
    print('Div = ' + i.__str__())
    list[i].click()
    # playButton = driver.find_element_by_class_name('cliui-video__play_btn')
    # playButton.click()
    videos = driver.find_elements_by_class_name('cliui-video__video_box')
    vLen = len(videos)
    if vLen != 0:
        for j in range(vLen):
            print('video = ' + j.__str__())
            video = videos[j]
            videoSrc = video.get_attribute('src')
            print('url =' + videoSrc)
            http = urllib3.PoolManager()
            response = http.request('GET', videoSrc)
            pageName = driver.__getattribute__('title')
            path = rootPath + pageName + '/'
            if not os.path.exists(path):
                os.mkdir(path)
            f = open(path + str(j) + '.mp4', 'wb')
            f.write(response.data)
            f.close()
            response.release_conn()
        docs = driver.find_elements_by_class_name('weui-cell_access')
        docLen = len(docs)
        for k in range(0, docLen):
            print('doc = ' + k.__str__())
            doc = docs[k]
            doc.click()
            while (1):
                try:
                    driver.find_element_by_class_name('download').click()
                    break
                except Exception:
                    pass
            time.sleep(1)
            driver.back()
            time.sleep(0.5)
            docs = driver.find_elements_by_class_name('weui-cell_access')
        driver.back()

    list = driver.find_elements_by_class_name('weui-cell_nav_p')
driver.close()
print('done')

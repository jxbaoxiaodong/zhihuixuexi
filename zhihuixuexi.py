# -*- coding: utf-8 -*-
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


print("2023智慧学习平台 心理健康内容 for 珊哥")
print("")
try:
    print("请输入以下信息，并按回车")
    sn=input("帐号：")
    code=input("密码：")
    print("***本次使用账号：",sn,"密码：",code)
except:
    print("请正确输入账号密码")
try:
    speed=input("设置播放倍速，默认10：")
    if len(speed)==0:
        speed=10
    else:
        speed=int(float(speed)) if int(float(speed))>=1 else 1
    print("***本次播放倍速",speed)
except:
    print("请正确设置倍速")
try:
    
    #打开网站进行检索   
    options=Options()
    options.add_argument('log-level=3')#因报大量日志而添加，若有错误可删除
    #options.add_argument('--headless')
    #options.addArguments("--window-size=1960,1080");#headless下最大化
    #登录
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()#窗口最大化避免有些元素单击不了,网页问题
    driver.get('https://www.zxx.edu.cn/ucAccount?redirect_uri=https%3A%2F%2Fwww.zxx.edu.cn%2F&signUp=false') #登录
    print("进入登录界面")
    time.sleep(6) 
    driver.switch_to.frame(0)
    driver.find_element(By.XPATH,'//*[@id="loginName"]').send_keys(sn) #
    time.sleep(1) 
    driver.find_element(By.XPATH,'//*[@id="password"]').send_keys(code) #
    time.sleep(1) 
    driver.find_element(By.XPATH,'//*[@id="agreementCheck"]').click()
    time.sleep(2) 
    driver.find_element(By.XPATH,'//*[@id="app"]/div/div/div/div/div/div[1]/div[1]/form/div[3]/button').click()
    time.sleep(2)     
    try:
        #print(driver.find_element(By.CLASS_NAME,'error-message').text)
        if "错误" in driver.find_element(By.CLASS_NAME,'error-message').text:
            print("用户名或密码错误！")
            driver.quit()
    except:
        pass
    driver.switch_to.parent_frame() 
    print("已登录")
    time.sleep(10) 
    #学习心理健康
    driver.get('https://www.zxx.edu.cn/training/f30ac359-402a-4883-9f4a-07c0f8356aca') #心理健康
    print("开始学习心理健康内容")
    time.sleep(5) 
    #循环点击TAB"
    for page in range(1,5):
        driver.execute_script("window.scrollTo(window.pageXOffset, 0)") #返回顶部 避免无法点击tab
        if page ==4:
            driver.execute_script("window.scrollTo(document.body.scrollWidth, window.pageYOffset)") #滚动到最右否则无法点击
        driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div[2]/div/div[3]/div/div[1]/div[1]/div/div['+str(page)+']').click()
        title=driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div[2]/div/div[3]/div/div[1]/div[1]/div/div['+str(page)+']').text    
        print("类别：",title)
        lianjie=driver.find_elements(By.CLASS_NAME,'index-module_title_8i8E6')
        for i in lianjie:
            if len(i.text)>0:
                i.click()
                time.sleep(10) 
                print("开始学习",i.text)
                wins =driver.window_handles
                driver.switch_to.window(wins[-1])
                time.sleep(5) 
                state=driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div/div/section/div/div[1]/div[3]/a').text
                #print(state)
                if "复习" in state:
                    print("此视频已学习")
                    driver.close()
                    time.sleep(1)
                    driver.switch_to.window(wins[0])
                    time.sleep(1)
                    continue
                driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div/div/section/div/div[1]/div[3]/a').click()#开始/继续观看
                time.sleep(5)
                try:
                    driver.find_element(By.XPATH,'//*[@id="main-content"]/div[3]/div[4]/div/div/micro-app/micro-app-body/div[2]/div/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div[1]/label/span[2]').click()
                    print("弹出学习指南")
                    time.sleep(15)
                    driver.find_element(By.XPATH,'//*[@id="main-content"]/div[3]/div[4]/div/div/micro-app/micro-app-body/div[2]/div/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div[2]').click()
                    time.sleep(5)
                    print("已关闭学习指南")
                except:
                    pass
                driver.find_element(By.XPATH,'//*[@id="vjs_video_1"]/button').click()
                duration=driver.find_element(By.CLASS_NAME,'vjs-control-text').text
                print("视频开始播放,时长:",duration)
                try:
                    driver.execute_script("document.getElementsByTagName ('video')[0].playbackRate = "+str(speed)) 
                    #driver.execute_script("document.querySelector('video').defaultPlaybackRate = 10") 
                    print("以"+str(speed)+"倍速播放")                
                except:
                    print("原速播放")                
                time.sleep(5)
                message="还没弹出答题窗口"
                while True:      
                    #判断是否弹出提示
                    try:
                        notetext=driver.find_element(By.CLASS_NAME,'fish-btn fish-btn-primary').text                    
                        if "知道" in notetext:
                            driver.find_element(By.CLASS_NAME,'fish-btn fish-btn-primary').click()
                            print("弹出提示")
                            break
                    except:
                        pass
                    #判断是否学完
                    try:
                        endtext=driver.find_element(By.CLASS_NAME,'course-video-reload').text                    
                        if "再学" in endtext:
                            print("视频已放完")
                            break
                    except:
                        pass
                    try:
                        testbox=driver.find_element(By.CLASS_NAME,'index-module_markerExercise_KM5bU').text                    
                        if testbox:
                            print(testbox)
                            time.sleep(1)
                            for i in range(3):
                                print("答题ing")
                                try:
                                    #判断题
                                    driver.find_element(By.CLASS_NAME,'nqti-option-radio-icon').click()#随便选第一个
                                    time.sleep(1)
                                except :
                                    try:
                                    #选择题
                                        driver.find_element(By.CLASS_NAME,'size').click()#随便选第一个
                                        time.sleep(1)
                                    except:
                                        pass
        
                                #点击下一题：
                                try:
                                    driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div/div/div[3]/div[1]/div[1]/div/div[2]/div/div[3]/button').click()
                                    time.sleep(1)
                                except:
                                    pass
                                #答题完成
                                try:
                                    driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div/div/div[3]/div[1]/div[1]/div/div[2]/div/div[3]/button').click()
                                    time.sleep(1)
                                except:
                                    pass
                        message="视频还没放完"
                    except:
                        time.sleep(10)
                        print(message)     
                driver.close()
                driver.switch_to.window(wins[0])
                time.sleep(1)
    
    print("都学完了!")
    input("按任意键退出......")
except:
    print("出现错误！请检查是否安装chrome浏览器，或者账号密码是否正确")
    input("按任意键退出......")


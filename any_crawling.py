from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

import warnings
warnings.filterwarnings('ignore')



options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)


driver.get('https://laftel.net/finder')
driver.implicitly_wait(3)
driver.maximize_window()

time.sleep(3)   

fbody  = driver.find_elements(By.CLASS_NAME, 'simplebar-content-wrapper')[1]
last_height = driver.execute_script("return arguments[0].scrollHeight", fbody)

while True:
    
  print('스크롤 중...')
  driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight-1000", fbody) # 화면크깅 따라 scrollHeight-1000 조절 
  time.sleep(3)
  
  driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", fbody)
  scrollTop =  driver.execute_script("return arguments[0].scrollTop", fbody)
  
  time.sleep(3)
  
  
  new_height = driver.execute_script("return arguments[0].scrollHeight", fbody)
  
  print('new_height: ', new_height, 'last_height: ', last_height, 'scrollTop', scrollTop)


  if new_height == scrollTop:
    break
  
  elif last_height == new_height:
      break

  last_height = new_height
  time.sleep(3)
  





제목_lst = []
장르_lst = []
줄거리_lst = []



all_contents = driver.find_elements(By.XPATH,'//*[@id="root"]/div[2]/div[2]/div[2]/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/a')
                                             

i = 0
for 애니 in all_contents:
    i+=1
    try:
        링크 = 애니.click()
        time.sleep(5)
        
        
        
        
        제목 = 애니.find_element(By.XPATH,'//*[@id="item-modal"]/div[1]/div/div[2]/div/header/h1').text
        
        장르 = 애니.find_element(By.XPATH,'//*[@id="item-modal"]/div[1]/div/div[2]/div/header/div/span[1]').text
    
        줄거리 = 애니.find_element(By.XPATH,'//*[@id="item-modal"]/div[1]/div/div[2]/div/div/section/article/summary').text
        print(줄거리,장르,제목)
        
        애니.find_element(By.XPATH,'//*[@id="item-modal"]/div[1]/div/div[2]/nav/button[2]').click()
        time.sleep(5)
        
        사진 = 애니.find_element(By.XPATH,'//*[@id="root"]/div[2]/div[2]/div[2]/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/a')
        
        img_url = 애니.find_element(By.XPATH, './div/div[1]/div/picture/img').get_attribute('src')

        img_path = r'C:\kdt c\deepimg' + '\\' + 제목 + ".jpg"
        r = requests.get(img_url, headers= { "User-Agent":"Mozilla/5.0"})
        with open(img_path, 'wb') as outfile:
            outfile.write(r.content)
        
        
        제목_lst.append(제목)
        장르_lst.append(장르)
        줄거리_lst.append(줄거리)
        
        
        
        

    
    except:
        print(f'***{i}번째 애니 에러 발생!!!')        
        
        
        
dict_df = {'title':제목,
           'genre': 장르,
           'summary':줄거리}
  
df_any = pd.DataFrame(dict_df)

file_name = r'C:\kdt c\deep_data\df_any.csv'
df_any.to_csv(file_name, index = False, encoding = 'UTP-8')






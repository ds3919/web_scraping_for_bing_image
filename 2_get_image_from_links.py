from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd
from tqdm import tqdm
import time

csv_path = 'image_results.csv'

df = pd.read_csv(csv_path, encoding='latin1')
df = df.drop_duplicates(subset='urls')
pages = df['urls'].tolist()
categories = df['word'].tolist()
current_page_index = 0

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=options)

images_url_list = []

for cat, link in tqdm(zip(categories, pages), total=len(categories)):

    url = link
    driver.get(url)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'img')))
    images = driver.find_elements(By.TAG_NAME, 'img')
    largest_image = None
    max_area = 0

    time.sleep(0.1)

    for image in images:
        try:
            width = int(image.get_attribute('width') or 0)
            height = int(image.get_attribute('height') or 0)
            area = width * height
            if area > max_area:
                max_area = area
                largest_image = image
        except StaleElementReferenceException:
            images = driver.find_elements(By.TAG_NAME, 'img')
            continue
        
        try:
            image_url = largest_image.get_attribute('src')
            images_url_list.append(image_url)
        except:
            images_url_list.append(None)

df["urls"] = images_url_list
df["categorization"] = [None] * len(images_url_list)
df_cleaned = df.dropna(subset=["urls"])

df_cleaned.to_csv("image_results_fixed.csv", encoding='latin1')
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException
#_11pzQk

#https://www.flipkart.com/search?q=red+dress

# {
    
#     "myntra" : [
#         [
#             "jeans url",
#             "top url"
#         ],
#         [
#             "skirt url",
#             "jacket url"
#         ]
#     ],
    
#     "flipkart" : [
#         [
            
#         ]
#     ],
#     "savana" : [
        
#     ]
    
# }
                  
def scrape_first_3_reviews_flipkart(url):
    chrome_options = webdriver.ChromeOptions()
    prefs = {"download.prompt_for_download": False,
            "safebrowsing.enabled": True}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    wait = WebDriverWait(driver, 20)
    
    reviews_data = []

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 3);")
    time.sleep(2)

    #handling missing rating and getting the reviews
    try:
        rating_elem = driver.find_element(By.CSS_SELECTOR, ".XQDdHH._6er70b")
        rating = rating_elem.text
    except NoSuchElementException:
        rating = "No rating available"

    #fetching reviews
    try:
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[6]/div[3]/div/div[1]')
        ))
        time.sleep(1)
        review_elements = driver.find_elements(By.CSS_SELECTOR, "div._11pzQk")
        review_texts = [elem.text for elem in review_elements[:3]]
        if not review_texts:
            review_texts = ["No reviews available"]
    except (NoSuchElementException, TimeoutException):
        review_texts = ["No reviews available"]

    reviews_data.append({
        "url": url,
        "review": review_texts,
        "rating": rating
    })

    driver.quit()
    return reviews_data

def scrape_first_3_reviews_myntra(url):
    from selenium.common.exceptions import NoSuchElementException
    chrome_options = webdriver.ChromeOptions()
    prefs = {"download.prompt_for_download": False,
            "safebrowsing.enabled": True}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    wait = WebDriverWait(driver, 20)

    reviews_data = []

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 3);")
    time.sleep(2)

    #extracting rating
    try:
        rating_elem = driver.find_element(By.CLASS_NAME, "index-averageRating")
        rating = rating_elem.text
    except NoSuchElementException:
        rating = "no review available"

    #extracting reviews
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="mountRoot"]/div/div[1]/main/div[2]/div[2]/main/div/div')))
        time.sleep(1)
        review_elements = driver.find_elements(By.CLASS_NAME, "user-review-reviewTextWrapper")
        review_texts = [elem.text for elem in review_elements[:3]]
        if not review_texts:
            review_texts = ["no review available"]
    except Exception:
        review_texts = ["no review available"]

    reviews_data.append({
        "url": url,
        "review": review_texts,
        "rating": rating
    })

    driver.quit()
    return reviews_data

def scrape_first_3_reviews_tatacliq(url):
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    chrome_options = webdriver.ChromeOptions()
    prefs = {"download.prompt_for_download": False,
            "safebrowsing.enabled": True}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    wait = WebDriverWait(driver, 20)
    
    reviews_data = []

    #scrolling down the page to load dynamic content
    for _ in range(6):
        driver.execute_script("window.scrollBy(0, window.innerHeight / 2);")
        time.sleep(1)

    try:
        #getting the the overall rating
        rating_elem = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[3]/div/div[2]/div/div/div[2]/div[2]/div[1]/div[1]/div[1]'))
        )
        rating = rating_elem.text.strip() or "no rating available"
    except (TimeoutException, NoSuchElementException):
        rating = "no rating available"

    try:
        #try exception block to get reviews
        review_elements = driver.find_elements(By.CLASS_NAME, "ReviewPage__text")
        review_texts = [elem.text.strip() for elem in review_elements if elem.text.strip()]
        if not review_texts:
            review_texts = ["no review available"]
    except Exception:
        review_texts = ["no review available"]

    reviews_data.append({
        "url": url,
        "review": review_texts,
        "rating": rating
    })

    driver.quit()
    return reviews_data


def combine_all(scraped_data):
    grouped_reviews = {}

    print('\n\n\n REVIEW SCRAPED DATA', scraped_data)

    for platform, batches in scraped_data.items():
        print('PLATFORM', platform)
        platform_reviews = []

        for batch in batches:
            print('\n\n\n BATCH', batch)
            batch_reviews = []

            for item in batch:
                if not isinstance(item, list) or not item or not isinstance(item[0], dict):
                    print('Skipping invalid item:', item)
                    continue

                url = item[0].get("product_link")
                print('Extracted URL:', url)

                if not url:
                    continue

                if platform == "flipkart":
                    reviews = scrape_first_3_reviews_flipkart(url)
                elif platform == "myntra":
                    reviews = scrape_first_3_reviews_myntra(url)
                elif platform == "tata":
                    reviews = scrape_first_3_reviews_tatacliq(url)
                else:
                    reviews = []

                for review in reviews:
                    batch_reviews.append({
                        "url": url,
                        "review": review.get("review", []),
                        "rating": review.get("rating", "no rating available"),
                        "name" : item[0].get("name"),
                        "description" : item[0].get("description"),
                        "price": item[0].get("price")
                    })

            platform_reviews.append(batch_reviews)

        grouped_reviews[platform] = platform_reviews

    return grouped_reviews
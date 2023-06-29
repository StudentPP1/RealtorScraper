from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import csv

options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

urls = ["https://directory.dmagazine.com/search/?sections=Residential+Real+Estate+Agents&awards=Best+Real+Estate+Agents+%3E+2023",
"https://directory.dmagazine.com/search/?sections=Residential+Real+Estate+Agents&awards=Best+Real+Estate+Agents+%3E+2022"]


def get_realtor_urls(list_urls: list[str]) -> list:
    realtor_urls = []

    for url in list_urls:
        driver.get(url)
        driver.implicitly_wait(5)

        end_page = driver.find_element(By.CLASS_NAME, "dir-pagination-wrapper")\
            .find_element(By.CLASS_NAME, "dir-pagination-status")\
            .find_elements(By.CLASS_NAME, "dir-pagination-status__number")[-1].text

        for current_page in range(int(end_page)):
            print(f"Current page: {current_page + 1} / {end_page}")
            driver.refresh()
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)

            for realtor_url in driver.find_elements(By.CLASS_NAME, "dir-card__link-overlay"):
                realtor_urls.append(realtor_url.get_attribute('href'))

            driver.find_element(By.CLASS_NAME, "pagination__numbers")\
                .find_elements(By.CLASS_NAME, "pagination__number ")[1].click()  # next page
            driver.implicitly_wait(5)

    return realtor_urls


def get_realtor_personal_data(url):
    driver.get(url)
    driver.implicitly_wait(5)

    try:
        name = driver.find_element(By.CLASS_NAME, "dir-title").text
    except Exception as ex:
        name = "N/A"

    try:
        phone_number = driver.find_element(By.CLASS_NAME, "js-template-listing-location")\
            .find_elements(By.CLASS_NAME, "dir-block__item")[-1].find_element(By.TAG_NAME, 'a')\
            .get_attribute("href").split(':')[-1]
    except Exception as ex:
        phone_number = "N/A"

    try:
        realtor_agency = driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[1]/div/div[3]").text\
            .replace("Company: ", '')
    except Exception as ex:
        realtor_agency = "N/A"

    print(name, realtor_agency, phone_number)
    return name, realtor_agency, phone_number


def main():
    with open("data.csv", 'w') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                "Name",
                "Agency",
                "Phone"
            )
        )

    realtor_urls = set(get_realtor_urls(urls))

    for realtor_url in realtor_urls:
        name, realtor_agency, phone_number = get_realtor_personal_data(realtor_url)

        with open("data.csv", 'a') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    name,
                    realtor_agency,
                    phone_number
                )
            )


if __name__ == "__main__":
    main()

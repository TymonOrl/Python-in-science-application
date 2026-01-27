from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time
import tqdm
import json

def accept_cookies(driver):
    found = False

    # first try main document
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//button[@title='Accept']"))
        )
        print("Accept button FOUND (main DOM)")
        WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@title,'Accept')]"))
        ).click()
        print("Accept button CLICKED")
        found = True
    except TimeoutException:
        pass

    # if not found, try iframes
    if not found:
        for iframe in driver.find_elements(By.TAG_NAME, "iframe"):
            driver.switch_to.frame(iframe)
            try:
                WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located((By.XPATH, "//button[@title='Accept']"))
                )
                print("Accept button FOUND (inside iframe)")
                WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@title,'Accept')]"))
                ).click()
                print("Accept button CLICKED")
                found = True
                driver.switch_to.default_content()
                break
            except TimeoutException:
                driver.switch_to.default_content()

    if not found:
        print("Accept button NOT found anywhere")


def extract_cell_value(td):
    # 1) If there is an <img>, try alt/aria-label/title (podium icons often use this)
    '''
    imgs = td.find_elements(By.CSS_SELECTOR, "img")
    if imgs:
        for attr in ("alt", "aria-label", "title"):
            v = (imgs[0].get_attribute(attr) or "").strip()
            if v:
                return v
        # sometimes the parent has aria-label
        for attr in ("aria-label", "title"):
            v = (td.get_attribute(attr) or "").strip()
            if v:
                return v
    '''
    # 2) Otherwise, grab all visible text in the cell (works for nested spans)
    txt = (td.get_attribute("textContent") or "").strip()
    # normalize whitespace a bit
    txt = " ".join(txt.split())
    return txt

def make_headers_unique(headers):
    seen = {}
    out = []

    for h in headers:
        if h not in seen:
            seen[h] = 1
            out.append(h)

    return out


if __name__== "__main__":
    KEEP_IDXS = [1, 3, 4, 5, 6, 7, 8]
    driver = webdriver.Chrome()
    driver.get("https://www.speedrun.com/mc")

    wait = WebDriverWait(driver, 5)

    driver.implicitly_wait(10)

    accept_cookies(driver)

    driver.implicitly_wait(5)

    print("Page title:", driver.title)
    table = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "table.w-full.whitespace-nowrap")
    ))
    print("Table found")

    header_divs = table.find_elements(
        By.CSS_SELECTOR,
        "tr.h-12.bg-panel th div"
    )

    headers = [
        (d.get_attribute("textContent") or "").strip()
        for d in header_divs
        if (d.get_attribute("textContent") or "").strip()
    ]

    headers = make_headers_unique(headers)
    print("Headers:", headers)

    rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
    print("Row count:", len(rows))

    all_rows = []
    for r in tqdm.tqdm(rows, desc="Processing rows"):
        tds = r.find_elements(By.CSS_SELECTOR, "td")
        all_rows.append([extract_cell_value(td) for td in tds])

    # quick preview
    filtered_rows = []
    for i, row in enumerate(all_rows):
        tmp_lst = []
        tmp_lst.append(i+1)  # add rank number
        for idx in KEEP_IDXS:
            tmp_lst.append(row[idx])

        filtered_rows.append(tmp_lst)

    data = []

    for row in filtered_rows:
        # ensure row length matches header length
        row_dict = {
            headers[i]: row[i]
            for i in range(min(len(headers), len(row)))
        }
        data.append(row_dict)


    output_path = "speedrun_mc.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(data)} rows to {output_path}")

    driver.implicitly_wait(5)

    driver.close()
import time
import datetime
from io import BytesIO
from PIL import Image, ImageOps
import pytesseract
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import schedule


TESSERACT_PATH = r"C:\BaiTapLon_TuDongHoaQuyTrinh\New folder\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

URL = "https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.html"
WHITELIST = 'abcdefghijklmnopqrstuvwxyz0123456789'


VEHICLES = [
    ("47F00171", "Ô tô"),
    ("98D1-60554", "Xe máy")
]


def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


def enhance_image(image):
    gray = image.convert("L")
    inverted = ImageOps.invert(gray)
    contrast = ImageOps.autocontrast(inverted)
    threshold = contrast.point(lambda x: 0 if x < 150 else 255, mode='1')
    resized = threshold.resize((threshold.width * 3, threshold.height * 3), Image.LANCZOS)
    return resized


def read_captcha_from_element(driver, element):
    try:
        driver.execute_script("arguments[0].scrollIntoView();", element)
        screenshot = Image.open(BytesIO(driver.get_screenshot_as_png()))
        loc = element.location_once_scrolled_into_view
        size = element.size
        scale_x = screenshot.width / driver.execute_script("return window.innerWidth")
        scale_y = screenshot.height / driver.execute_script("return window.innerHeight")

        box = (
            int(loc["x"] * scale_x),
            int(loc["y"] * scale_y),
            int((loc["x"] + size["width"]) * scale_x),
            int((loc["y"] + size["height"]) * scale_y)
        )
        captcha_img = screenshot.crop(box)
        processed_img = enhance_image(captcha_img)

        for psm in [8, 7]:
            config = f'--psm {psm} --oem 3 -c tessedit_char_whitelist={WHITELIST}'
            result = pytesseract.image_to_string(processed_img, config=config).lower().strip()
            result = ''.join(filter(str.isalnum, result))
            if len(result) == 6:
                print(f"[OK] Nhận diện captcha thành công: {result}")
                return result
            else:
                print(f"[FAIL] Sai captcha ({config}): {result}")
    except Exception as e:
        print(f"[ERROR] Lỗi OCR: {e}")
    return None


def go_to_website_and_fill_form(driver, bien_so, loai_xe):
    driver.get(URL)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "BienKiemSoat"))).clear()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "BienKiemSoat"))).send_keys(bien_so)

    loai_xe_select = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "LoaiXe")))
    for option in loai_xe_select.find_elements(By.TAG_NAME, "option"):
        if option.text.strip().lower() == loai_xe.lower():
            option.click()
            break

    return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "imgCaptcha")))


def submit_captcha_and_get_result(driver, captcha_code, bien_so, loai_xe):
    captcha_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "txt_captcha")))
    captcha_input.clear()
    captcha_input.send_keys(captcha_code)
    driver.find_element(By.CLASS_NAME, "btnTraCuu").click()

    try:
        result_element = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.ID, "bodyPrint123")))
        result = result_element.text.strip()
        if "Biển kiểm soát" in result and "Thời gian vi phạm" in result:
            print(f"[KẾT QUẢ] Đã tìm thấy vi phạm cho {loai_xe} {bien_so}!")
            print(result)
            return True
        else:
            print("Không có dữ liệu hoặc sai captcha.")
    except:
        print("Không tìm thấy kết quả hoặc hệ thống lỗi.")
    return False


def tra_cuu_vi_pham(bien_so, loai_xe):
    driver = init_driver()
    try:
        for attempt in range(5):
            print(f"\nThử lần {attempt + 1} cho {loai_xe} {bien_so}")
            try:
                captcha_img = go_to_website_and_fill_form(driver, bien_so, loai_xe)
                captcha_code = read_captcha_from_element(driver, captcha_img)
                if not captcha_code:
                    print("Không đọc được captcha, thử lại...")
                    continue

                if submit_captcha_and_get_result(driver, captcha_code, bien_so, loai_xe):
                    return
            except Exception as e:
                print(f"[ERROR] Lỗi form hoặc trang web: {e}")
            time.sleep(2)
    finally:
        driver.quit()


def job():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\nĐang tra cứu lúc {now}")
    for plate, vehicle in VEHICLES:
        tra_cuu_vi_pham(plate, vehicle)

if __name__ == "__main__":
    schedule.every().day.at("06:00").do(job)
    schedule.every().day.at("12:00").do(job)
    print("Hệ thống sẽ tra cứu tự động lúc 06:00 và 12:00 mỗi ngày cho ô tô và xe máy.")
    while True:
        schedule.run_pending()
        time.sleep(1)

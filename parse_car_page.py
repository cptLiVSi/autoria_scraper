import re
import requests
from datetime import datetime as dt, UTC
from bs4 import BeautifulSoup
import logging


logger = logging.getLogger(__name__)

def parse_car_page(url: str, headers) -> dict:
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')

    def extract(selector):
        el = soup.select_one(selector)
        return el.get_text(strip=True) if el else None

    def get_phone_number():
        data_auto_id = soup.body.get('data-auto-id')
        tag_with_hash = soup.find(attrs={"data-hash": True})
        data_hash = tag_with_hash['data-hash']
        data_expires = tag_with_hash['data-expires']
        phone_request_url = f"https://auto.ria.com/users/phones/{data_auto_id}?hash={data_hash}&expires={data_expires}"
        response = requests.get(phone_request_url, headers=headers)
        data = response.json()
        return "+38" + re.sub(r"\D", "", data['formattedPhoneNumber'])


    title = extract('h1.head')

    price_usd = extract('span[data-currency="USD"]') or extract('.price_value strong')
    price_usd = int(price_usd.replace(" ", "").replace("$", ""))

    odometer_text = extract('.base-information span.size18')
    odometer = int(float(odometer_text.replace(' ', ''))) * 1000 if odometer_text else None

    username = extract('.seller_info_name') or extract('.seller_info_link')

    phone_number = get_phone_number()

    image_tag = soup.select_one('div.carousel-inner img')
    image_url = image_tag['src']

    images_count_text = extract("div.action_disp_all_block > a")
    match = re.search(r'\d+', images_count_text or "")
    images_count = int(match.group()) if match else 0

    car_number_tag = soup.select_one("div.t-check span.state-num")
    car_number = car_number_tag.contents[0].strip() if car_number_tag else None
    if not car_number:
        logger.warning(f"no car number for {url}")

    car_vin_tag = soup.select_one("span.label-vin")
    car_vin = car_vin_tag.text.strip() if car_vin_tag else None
    if not car_vin:
        logger.warning(f"no VIN for {url}")


    result = {
        "url": url,
        "title": title,
        "price_usd": price_usd,
        "odometer": odometer,
        "username": username,
        "phone_number": phone_number,
        "image_url": image_url,
        "images_count": images_count,
        "car_number": car_number,
        "car_vin": car_vin,
        "datetime_found": dt.now(UTC).isoformat()
    }

    return result
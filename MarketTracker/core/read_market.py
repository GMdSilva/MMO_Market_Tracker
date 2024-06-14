import pytesseract
import pandas as pd
from datetime import datetime

from helpers.game_interaction.vision import Vision, process_image, read_image_text
from configs.cons import MARKET_COORDS
from helpers.utils import write_coin_price

# Initialize Vision
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
vs = Vision()


def read_offer_data(read_coords):
    img = vs.capture_text(read_coords, update=True)
    processed_imgs = process_image(img, rescale_factor=3)
    return processed_imgs


def do_ocr(processed_imgs):
    ocr_data = []
    for img_fragment in processed_imgs:
        ocr_data.append(read_image_text(img_fragment))
    return ocr_data


def extract_offer_data(offer_type):
    data = {}
    for key, coords in MARKET_COORDS[offer_type].items():
        rectangle = read_offer_data(coords)
        text = do_ocr(rectangle)
        data[key] = [item.strip() for item in text]
    return data


def sanitize_string(input_string):
    try:
        sanitized_string = ''.join(char for char in input_string if char.isdigit())
    except:
        sanitized_string = input_string
    if sanitized_string == '':
        sanitized_string = 100000000
    return int(sanitized_string)


def build_dataset(item_name, folder_name):
    top_offer_coins = []
    for offer_type in ['ask', 'bid']:
        data = extract_offer_data(offer_type)

        dates = data['DAY_COORDS']
        hours = data['HOUR_COORDS']
        collated = [f'{date}-{hour}' for date, hour in zip(dates, hours)]

        offer_ids = []
        for price, timestamp in zip(data['PRICE_COORDS'], collated):
            offer_ids.append(f'{price}_{timestamp}')

        df = pd.DataFrame({
            'order_n': range(len(data['AMOUNT_COORDS'])),
            'quantity': data['AMOUNT_COORDS'],
            'prices': data['PRICE_COORDS'],
        })

        quantities = []
        prices = []
        for quantity, price in zip(df['quantity'], df['prices']):
            quantities.append(sanitize_string(quantity))
            prices.append(sanitize_string(price))

        df['quantity'] = quantities
        df['prices'] = (prices)
        df['total'] = df['quantity'] * df['prices']
        df['cur_time'] = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        df['offer_id'] = offer_ids

        if item_name == 'rubini_coins':
            top_offer_coins.append(df['prices'].iloc[0])

        df.to_csv(f"results/{folder_name}/{item_name}/{offer_type}_instant.csv", index=False)

    if item_name == 'rubini_coins':
        avg_coin_price = (top_offer_coins[0]+top_offer_coins[1])/2
        write_coin_price(avg_coin_price, f'results/{folder_name}/average_coin_price.json')

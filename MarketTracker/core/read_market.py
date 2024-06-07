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
    processed_img = process_image(img, rescale_factor=3)
    return processed_img


def do_ocr(processed_img):
    ocr_data = read_image_text(processed_img)
    return ocr_data


def extract_offer_data(offer_type):
    data = {}
    for key, coords in MARKET_COORDS[offer_type].items():
        rectangle = read_offer_data(coords)
        text = do_ocr(rectangle)
        data[key] = [value.strip() for value in text.split('\n') if value.strip()]
    return data


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

        df['quantity'] = df['quantity'].astype(int)
        df['prices'] = df['prices'].astype(int)
        df['total'] = df['quantity'] * df['prices']
        df['cur_time'] = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        df['offer_id'] = offer_ids

        if item_name == 'rubini_coins':
            top_offer_coins.append(df['prices'].iloc[0])

        df.to_csv(f"results/{folder_name}/{item_name}/{offer_type}_instant.csv", index=False)

    if item_name == 'rubini_coins':
        avg_coin_price = (top_offer_coins[0]+top_offer_coins[1])/2
        write_coin_price(avg_coin_price, f'results/{folder_name}/average_coin_price.json')

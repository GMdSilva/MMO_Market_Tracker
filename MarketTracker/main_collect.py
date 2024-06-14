import time

from helpers.game_interaction import game_actions
from core.read_market import build_dataset
from core.save_market import read_and_append_unique
from helpers.utils import create_output_folder
from configs.cons import CURRENT_DATE, ASSETS


def process_assets(assets):
    """
    Process each asset by interacting with the game, building the dataset,
    and appending market data.
    """
    while True:
        for asset in assets:
            asset_for_game = asset.replace("_", " ")
            game_actions.input_item_name(asset_for_game)
            time.sleep(1)
            game_actions.click_market_offers()
            time.sleep(0.25)
            build_dataset(asset, CURRENT_DATE)
            read_and_append_unique(asset, CURRENT_DATE)


def main():
    for asset in ASSETS:
        create_output_folder(f'results/{CURRENT_DATE}/{asset}')
    process_assets(ASSETS)


if __name__ == '__main__':
    main()

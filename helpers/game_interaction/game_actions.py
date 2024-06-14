""""""

from __future__ import annotations

import time
from typing import Callable

from configs import cons
from helpers.game_interaction import stealth_interface
from helpers.utils import spell_out_string


def click_top_item_thumb():
    """ Clicks center of thumbnail on the topmost position of the Tibia market menu """
    stealth_interface.stealth_left_click(cons.COORDS['item_query'][0], cons.COORDS['item_query'][1])


def click_item_area():
    """ Clicks item thumbnail area of the Tibia market menu """
    stealth_interface.stealth_left_click(cons.COORDS['send_item_area'][0], cons.COORDS['send_item_area'][1])


def click_item_name_clear_button():
    """ Resets text in the item name input box in the Tibia main Market window """
    stealth_interface.stealth_left_click(cons.COORDS['x_button'][0], cons.COORDS['x_button'][1])


def click_market_offers():
    """ Resets text in the item name input box in the Tibia main Market window """
    stealth_interface.stealth_left_click(cons.COORDS['ask_last_offer'][0], cons.COORDS['ask_last_offer'][1])
    stealth_interface.stealth_left_click(cons.COORDS['bid_last_offer'][0], cons.COORDS['bid_last_offer'][1])


def run_game_action_safely(fun: Callable) -> Callable:
    """ When orders are completed, a pop-up window appears, this function closes it before running a game function

    Args:
        fun: any game-related function that you want to run safely, meaning not have the pop-up interact with it

    Returns:
        fun: any game-related function that you want to run safely, meaning not have the pop-up interact with it

    """
    bye_confirmation_box()
    return fun()


def bye_confirmation_box():
    """ When orders are completed, a pop-up window appears, this function closes it by pressing enter """
    time.sleep(0.1)
    stealth_interface.send_enter()


def input_item_name(item_name: str):
    """ Writes the name of the item we want to buy or sell inside the main Tibia Market window

    Args:
        item_name: name for the item to be bought or sold

    """
    run_game_action_safely(lambda: click_item_name_clear_button())  # clears name box #
    time.sleep(0.1)
    run_game_action_safely(lambda: click_item_area())  # make sure we are within the right market area #
    time.sleep(0.1)
    spelled_out_dict = {item_name: spell_out_string(item_name)}
    run_game_action_safely(lambda: stealth_interface.stealth_send_key(spelled_out_dict[item_name]))  # send keys #
    time.sleep(0.1)
    run_game_action_safely(lambda: click_top_item_thumb())  # clicks item #
    time.sleep(0.1)

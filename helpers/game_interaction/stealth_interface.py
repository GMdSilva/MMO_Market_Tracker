import time

from helpers.game_interaction.vision import StealthMode

wi = StealthMode()


def stealth_left_click(x: int, y: int):
    """ Stealthily (without hijacking cursor) left-clicks

    Args:
        x: first coordinate of click point (x)
        y: second coordinate of click point (y)

    """
    wi.click((x, y), 'left')
    time.sleep(0.1)


def fast_left_click(x: int, y: int):
    """ Stealthily (without hijacking cursor) left-clicks

    Args:
        x: first coordinate of click point (x)
        y: second coordinate of click point (y)

    """
    wi.click((x, y), 'left')
    # time.sleep(0.1)


def stealth_right_click(x: int, y: int):
    """ Stealthily (without hijacking cursor) right-clicks

    Args:
        x: first coordinate of click point (x)
        y: second coordinate of click point (y)

    """
    wi.click((x, y), 'right')
    time.sleep(0.1)


def stealth_send_key(key: str):
    """ Stealthily (without hijacking cursor) sends key

    Args:
        key: keyboard key to be sent

    """
    wi.send_keys(key)
    time.sleep(0.1)
    # keyboard.press_and_release(key)


def stealth_delete():
    """ Stealthily (without hijacking cursor) sends delete """
    wi.delete()
    time.sleep(0.1)


def send_enter():
    """ Stealthily (without hijacking cursor) sends enter """
    wi.send_enter()
    time.sleep(0.1)

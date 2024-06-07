from ctypes import windll
import numpy as np
import win32api
import win32con
import win32gui
import win32ui
from PIL import Image

from configs import cons


class StealthMode(object):
    """ Defines functions used to interface with Windows stealthily (without losing control of cursor or keyboard) """

    def __init__(self):
        self.hwnd = self.get_handle()  # Get Windows window handle for the window we are going to interact with #

    @staticmethod
    def get_handle(char_name: str = cons.CHAR_NAME) -> int:
        """ Gets the numeric handle of a window in the Windows OS by searching for a character name,
        this works for Tibia because the Tibia window has a title in the format "Tibia - <Character name>"

        Args:
            char_name (optional): character name that is going to be logged at the window we want to interact with
        Returns:
            hwnd: window handle (numeric) that Win32Api/Con/UI uses to locate specific windows

        """

        toplist, winlist = [], []

        def enum_cb(hwnd, _):
            """ Enumerates windows running at time of running and appends their handles and titles to list

            Args:
                hwnd: function to get handles
                _: doesn't do anything as far as I am aware, but EnumWindows needs it for some reason
            Returns:
                winlist.append: list containing windows titles and their respective handles

            """
            winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

        win32gui.EnumWindows(enum_cb, toplist)

        game_window = [(hwnd, title) for hwnd, title in winlist if char_name in title.lower()]
        game_handle = game_window[0]
        hwnd = game_handle[0]
        return hwnd

    def click(self, coords: tuple[int, int], button: str):
        """ Actually sends the stealth right-click to coordinate pair (x, y) if Tibia window is open and visible

        Args:
            coords: (x, y) tuple containing the coordinates to be right-clicked at
            button: kind of click ('left' or 'right')

        """

        if win32gui.IsWindowVisible(self.hwnd):
            if 'Tibia' in win32gui.GetWindowText(self.hwnd):
                # read_coords = win32gui.ScreenToClient(self.hwnd, read_coords)
                if button == 'left':
                    win32gui.PostMessage(self.hwnd, win32con.WM_LBUTTONDOWN, 0, win32api.MAKELONG(coords[0], coords[1]))
                    win32gui.PostMessage(self.hwnd, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(coords[0], coords[1]))
                else:
                    win32gui.PostMessage(self.hwnd, win32con.WM_RBUTTONDOWN, 0, win32api.MAKELONG(coords[0], coords[1]))
                    win32gui.PostMessage(self.hwnd, win32con.WM_RBUTTONUP, 0, win32api.MAKELONG(coords[0], coords[1]))

    def send_keys(self, msg: str):
        """ Actually sends the message to input (stealthily) if Tibia window is open and visible

        Args:
            msg: string containing the message to be sent to Tibia input forms

        """

        if win32gui.IsWindowVisible(self.hwnd):
            if 'Tibia' in win32gui.GetWindowText(self.hwnd):
                for c in msg:
                    win32api.SendMessage(self.hwnd, win32con.WM_CHAR, ord(str(c)), 0)

    def delete(self):
        """ Actually sends the delete command (backspace, stealthily) if Tibia window is open and visible """

        if win32gui.IsWindowVisible(self.hwnd):
            if 'Tibia' in win32gui.GetWindowText(self.hwnd):
                for i in range(0, 10):
                    win32api.SendMessage(self.hwnd, win32con.WM_KEYDOWN, win32con.VK_BACK, 0)
                    win32api.SendMessage(self.hwnd, win32con.WM_KEYUP, win32con.VK_BACK, 0)

    def send_enter(self):
        """ Actually sends the enter command (stealthily) if Tibia window is open and visible """

        if win32gui.IsWindowVisible(self.hwnd):
            if 'Tibia' in win32gui.GetWindowText(self.hwnd):
                win32api.SendMessage(self.hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
                win32api.SendMessage(self.hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)

    def background_screenshot(self) -> np.array:
        """ Takes screenshot of window defined by handle (hwnd), stealthily, and returns it in the form of numpy array

        Returns:
            im: numpy array containing the image we just screenshot
        """

        # Change the line below depending on whether you want the whole window
        # or just the client area.
        left, top, right, bot = win32gui.GetClientRect(self.hwnd)
        # left, top, right, bot = win32gui.GetWindowRect(hwnd)
        w = right - left
        h = bot - top

        hwnd_dc = win32gui.GetWindowDC(self.hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()

        save_bit_map = win32ui.CreateBitmap()
        save_bit_map.CreateCompatibleBitmap(mfc_dc, w, h)

        save_dc.SelectObject(save_bit_map)

        # Change the line below depending on whether you want the whole window
        # or just the client area.
        # result = windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 1)
        result = windll.user32.PrintWindow(self.hwnd, save_dc.GetSafeHdc(), 1)

        bmpinfo = save_bit_map.GetInfo()
        bmpstr = save_bit_map.GetBitmapBits(True)

        im = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)

        win32gui.DeleteObject(save_bit_map.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, hwnd_dc)

        if result == 1:
            im = np.array(im)
            im = im[:, :, ::-1].copy()
            return im

import pytesseract
from PIL import Image
from typing import *
import cv2
import numpy as np

from helpers.game_interaction.os_interface import StealthMode


class Vision(StealthMode):
    """ Reads resource values from Tibia Market Window (gold or gems) and returns them as an int
        StealthMode: stealth_interface object that defines methods for interacting with windows """

    def __init__(self):
        super(Vision, self).__init__()
        self.image: np.array = self.background_screenshot()

    def split_image_vertically(self):
        """ Splits the image into 6 equal vertical parts and saves them. """
        height, width, _ = self.image.shape
        part_width = width // 6
        parts = [self.image[:, i * part_width:(i + 1) * part_width] for i in range(6)]

        for idx, part in enumerate(parts):
            part_image = Image.fromarray(part)
            part_image.save(f'debug/part_{idx}.png')

    def capture_text(self, read_coords: List[int], update: bool = False, testing: bool = False) -> str:
        """ Captures text at specific part of screen, either taking a screenshot before or not,
        using pytesseract OCR and then returns either the whole read text or just the first line

        Args:
            read_coords: region in the screen to read, in the format (x, y, width, height)
            update (optional): either takes new screenshot before detecting (True) or not (False)
            testing (optional): testing new OCR parameters to improve detection
        Return:
            data: everything that was read
            lines[0]: just the first line that was read

        """

        x, y, w, h = (read_coords[0],
                      read_coords[1],
                      read_coords[2],
                      read_coords[3],)

        if update:
            self.image = self.background_screenshot()
        image = self.image[y:y + h, x:x + w]

        height, width, _ = image.shape
        part_height = height // 7
        parts = [image[i*part_height:(i+1)*part_height, :] for i in range(7)]

        for idx, part in enumerate(parts):
            part_image = Image.fromarray(part)
            part_image.save(f'debug/part_{idx}.png')

        imgs = []
        for img_fragment in parts[0:5]:
            if testing:
                img_fragment = cv2.resize(img_fragment, None, fx=2, fy=2)
            gray = cv2.cvtColor(img_fragment, cv2.COLOR_BGR2GRAY)
            sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
            sharpen = cv2.filter2D(gray, -1, sharpen_kernel)
            thresh = cv2.threshold(sharpen, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
            # OCR
            img = Image.fromarray(thresh)
            img.save(f'debug/{read_coords}debug.png')
            imgs.append(img)
        return imgs




def process_image(cropped_image: Image.Image, invert=True,
                  rescale_factor: int = 1) -> Image.Image:
    """
    Converts the image into a more AI readable format.
    relative_box in this format (relative_left, relative_top, relative_width, relative_height).
    """

    # cropped_image = cropped_image.convert("L")
    #
    # cropped_image.save("debug/selection_showcase.png")
    #
    # img = np.asarray(cropped_image, dtype="uint8")
    #
    # # Bigger images yield better accuracy with tesseract. Use this if OCR is yielding nonsense.
    # if rescale_factor > 0 and rescale_factor != 1:
    #     y, x = len(img), len(img[0])
    #     img = cv2.resize(img, [int(x * rescale_factor), int(y * rescale_factor)], interpolation=cv2.INTER_CUBIC)
    # img = cv2.threshold(img, 128, 255, (cv2.THRESH_BINARY_INV if invert else cv2.THRESH_BINARY) | cv2.THRESH_OTSU)
    #
    # # Force black text on white background.
    # if img[1][0][0] == 0:
    #     img = cv2.threshold(img[1], 128, 255, cv2.THRESH_BINARY_INV)
    #
    # cropped_image = Image.fromarray(img[1])

    return cropped_image


def read_image_text(image: Image.Image, psm: int = 7, oem: int = 1, char_white_list: str = "0123456789k-:,") -> str:
    """
    Feeds the image to tesseract, and returns the text it detected.
    """
    config = f"--oem {oem} --psm {psm} -c tessedit_char_whitelist={char_white_list}"

    try:
        return pytesseract.image_to_string(image, config=config)
    except pytesseract.TesseractNotFoundError as e:
        print(e)
        exit(1)

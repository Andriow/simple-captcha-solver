import cv2
import base64
import logging
import pytesseract

class Captcha(object):
    def __init__(self, logger: logging.Logger = None):
        super().__init__()
        self.className = 'Captcha'
        self.initializeLogger(logger=logger)

    def initializeLogger(self, logger: logging.Logger = None, level: int = logging.INFO) -> logging.Logger:
        if logger == None:
            self.logger = logging.getLogger(self.className)
            self.logger.setLevel(level)
            ch = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s [%(filename)s:%(lineno)d] - %(levelname)s - %(message)s")
            ch.setFormatter(formatter)
            ch.addFilter(logging.Filter(self.className))
            self.logger.addHandler(ch)
        else:
            self.logger = logger
            if self.logger.level != level:
                self.logger.setLevel(level)

    def create_img_file(self, imgstring:str):
        imgdata = base64.b64decode(imgstring)
        self.logger.info('Salvando a imagem no disco.')
        filename = 'captcha.jpg'  # I assume you have a way of picking unique filenames
        with open(filename, 'wb') as f:
            f.write(imgdata)

    def solver(self):
        self.logger.info('Solving the cpatcha using only openCV')
        # Grayscale, Gaussian blur, Otsu's threshold
        image = cv2.imread('captcha.jpg')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3,3), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Morph open to remove noise and invert image
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        invert = 255 - opening

        solved = pytesseract.image_to_string(invert, lang='eng', config='--psm 6')
        self.logger.info(f'captcha solved: {solved}')

        solved2 = pytesseract.image_to_string(invert, lang='eng', 
                                              config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz')
        self.logger.info(f'captcha solved2: {solved2}')

if __name__ == "__main__":
    captcha = Captcha()
    imgstring = b'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'
    captcha.create_img_file(imgstring=imgstring)
    captcha.solver()
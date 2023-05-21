import urllib.request
from PIL import Image
from io import BytesIO


class ImageParser:
    def __init__(self, data: dict):
        self.test_data = data
        self.byteImages = {}
        self.load_all_images()

    def get_image_bytes(self, url: str):
        """Возвращает байты изображения по ссылке"""
        response = urllib.request.urlopen(url)
        return response.read()

    def load_all_images(self):
        """Загружает все изображения в виде PIL.Image из теста в словарь"""
        for case, data in self.test_data["cases"].items():
            if "image" in data.keys():
                if len(data["image"]) > 0:
                    try:
                        image = self.get_image_bytes(data["image"])
                        self.byteImages[case] = Image.open(BytesIO(image))
                    except Exception as e:
                        continue

    def get_image_by_case(self, case: str):
        """Возвращает изображение по кейсу"""
        if case in self.byteImages.keys():
            return self.byteImages[case]
        return None


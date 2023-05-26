from PIL import Image
from urllib.parse import urlparse
from urllib import request
from io import BytesIO


class ImageParser:
    def __init__(self, data: dict):
        self.test_data = data
        self.byteImages = {}
        self.load_all_images()

    def get_url_image_bytes(self, url: str):
        """Возвращает байты изображения по ссылке"""
        response = request.urlopen(url)
        return response.read()

    def validate_url(self, url):
        """Проверяет ссылку на валидность"""
        parsed_url = urlparse(url)
        return all([parsed_url.scheme, parsed_url.netloc])

    def load_all_images(self):
        """Загружает все изображения в виде PIL.Image из теста в словарь"""
        for case, data in self.test_data["cases"].items():
            if "image" in data.keys():
                if len(data["image"]) > 0:
                    try:
                        if self.validate_url(data["image"]):
                            self.byteImages[case] = Image.open(BytesIO(self.get_url_image_bytes(data["image"])))
                        else:
                            self.byteImages[case] = Image.open(f"tests_images/{data['image']}")
                    except:
                        continue

    def get_image_by_case(self, case: str):
        """Возвращает изображение по кейсу"""
        if case in self.byteImages.keys():
            return self.byteImages[case]
        return None


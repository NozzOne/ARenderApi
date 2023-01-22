import base64
import urllib.request

import cv2
import numpy as np
import onnxruntime as rt


class ImageProcessing:

    def __init__(self, img) -> None:
        self.img = self.url_to_img(img) if self.detect_type(
            img) == 'url' else self.base64_to_img(img)
        self.output_img = None
        self.output_mask = None
        self.process()

    def detect_type(self, img: str) -> str:
        if img.startswith('http'):
            return 'url'
        elif img.startswith('data:image'):
            return 'base64'
        else:
            return 'unknown'

    def base64_to_img(self, base64_img: str) -> None:
        img = base64.b64decode(base64_img)
        img = np.frombuffer(img, np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        return img

    def url_to_img(self, url: str) -> None:
        r = urllib.request.urlopen(url)
        img = np.asarray(bytearray(r.read()), dtype="uint8")
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        return img

    def get_mask(self, img, s=1024):
        img = (img / 255).astype(np.float32)
        h, w = h0, w0 = img.shape[:-1]
        h, w = (s, int(s * w / h)) if h > w else (int(s * h / w), s)
        ph, pw = s - h, s - w
        img_input = np.zeros([s, s, 3], dtype=np.float32)
        img_input[ph // 2:ph // 2 + h, pw //
                  2:pw // 2 + w] = cv2.resize(img, (w, h))
        img_input = np.transpose(img_input, (2, 0, 1))
        img_input = img_input[np.newaxis, :]
        mask = self.model.run(None, {'img': img_input})[0][0]
        mask = np.transpose(mask, (1, 2, 0))
        mask = mask[ph // 2:ph // 2 + h, pw // 2:pw // 2 + w]
        mask = cv2.resize(mask, (w0, h0))[:, :, np.newaxis]
        return mask

    def rmbg_fn(self, img):
        mask = self.get_mask(img)
        img = (mask * img + 255 * (1 - mask)).astype(np.uint8)
        mask = (mask * 255).astype(np.uint8)
        img = np.concatenate([img, mask], axis=2, dtype=np.uint8)
        mask = mask.repeat(3, axis=2)
        return mask, img

    def process(self):
        providers = ['CPUExecutionProvider']
        self.model = rt.InferenceSession(
            "./app/core/model/isnetis.onnx", providers=providers)
        self.output_mask, self.output_img = self.rmbg_fn(
            self.img)

    def get_size(self, bytes: bytes):
        return len(bytes) / 1024

    @property
    def to_bytes(self):
        _, img_bytes = cv2.imencode('.png', self.output_img, [
            int(cv2.IMWRITE_PNG_COMPRESSION), 9])
        return img_bytes

    @property
    def to_base64(self):
        return base64.b64encode(self.to_bytes).decode()


__all__ = ["ImageProcessing"]

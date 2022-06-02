import typing
import torch
import torchvision
import numpy as np
from PIL import Image
from torch.autograd import Variable
from src.final_work.transformer import Transformer
from enum import Enum


class ModelType(Enum):
    HOSODA = "hosoda_mamoru"
    KON = "kon_satoshi"
    MIYAZAKI = "miyazaki_hayao"
    SHINKAI = "shinkai_makoto"


class Device(Enum):
    CPU = "cpu"
    GPU = torch.device("cuda")


class ImageConverter:
    MAX_IMAGE_SIZE = 1280
    MODELS_DIRECTORY = "models"

    def __init__(self):
        self.device = self._define_device()
        self._init_models()

    def _get_model(self, model_type: ModelType) -> Transformer:
        return self.models[model_type.value]

    @staticmethod
    def _define_device() -> Device:
        _is_gpu_enable = torch.cuda.is_available()
        if _is_gpu_enable:
            return Device.GPU
        else:
            return Device.CPU

    def _init_models(self):
        self.models = dict()
        for model_type in ModelType:
            self.models[model_type.value] = self._create_model(model_type)

    def _load_model_parameters(self, model: ModelType):
        return torch.load(f"{self.MODELS_DIRECTORY}/{model.value}.pth", self.device.value)

    def _create_model(self, model_type: ModelType) -> Transformer:
        new_model = Transformer()
        new_model_parameters = self._load_model_parameters(model_type)
        new_model.load_state_dict(new_model_parameters)

        if self.device == Device.GPU:
            new_model.to(self.device.value)

        new_model.eval()
        return new_model

    def convert_image(self, image: Image, model_type: ModelType) -> Image:
        image = image.convert("RGB")
        image = np.asarray(image)
        image = image[:, :, [2, 1, 0]]
        image = torchvision.transforms.ToTensor()(image).unsqueeze(0)
        image = -1 + 2 * image
        if self.device == Device.GPU:
            image = Variable(image).to(self.device.value)
        else:
            image = Variable(image).float()

        model = self._get_model(model_type)
        converted_image = model(image)
        converted_image = converted_image[0]
        converted_image = converted_image[[2, 1, 0], :, :]
        converted_image = converted_image.data.cpu().float() * 0.5 + 0.5

        return torchvision.transforms.ToPILImage()(converted_image)

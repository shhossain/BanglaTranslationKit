from bntrans.tools import sent_tokens_bangla, sent_tokens_english
from transformers import pipeline, AutoTokenizer, AutoConfig
from typing import Any, Literal, Optional
import warnings
import os
import requests
import time

model_config = {
    "shhossain/opus-mt-en-to-bn": {
        "max_position_embeddings": 128,
    },
    "Helsinki-NLP/opus-mt-bn-en": {
        "max_position_embeddings": 512,
    },
}


class CloudPipeline:
    def __init__(self, model: str, token: str):
        self.model = model
        self.token = token
        self.API_URL = f"https://api-inference.huggingface.co/models/{self.model}"
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def generate(self, inputs: list[str], wait_for_model: bool = False):
        response = requests.post(
            self.API_URL,
            headers=self.headers,
            json={"inputs": inputs, "wait_for_model": wait_for_model},
        )
        data = response.json()
        if "error" in data:
            if "currently loading" in data["error"]:
                time.sleep(1)
                return self.generate(inputs, wait_for_model=True)
            else:
                raise ValueError(data["error"])
        return data

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        inputs = None
        if "inputs" not in kwds:
            inputs = args[0]
        else:
            inputs = kwds["inputs"]

        return self.generate(inputs)


class Translator:
    def __init__(
        self,
        src: Literal["en", "bn"] = "en",
        dest: Literal["en", "bn"] = "bn",
        model: Optional[str] = None,
        use_gpu: bool = True,
        max_length: Optional[int] = None,
        default_models: Optional[dict[str, str]] = None,
        use_cloud: bool = False,
        huggingface_token: Optional[str] = None,
        **kw,
    ):
        """
        Translator class for translating text from one language to another.

        Parameters
        ----------
        src : Literal["en", "bn"], optional
            Source language, by default "en".
        dest : Literal["en", "bn"], optional
            Destination language, by default "bn".
        model : Optional[str], optional
            Model to use for translation, by default None. If None, a default model will be used.
        use_gpu : bool, optional
            Whether to use GPU for translation, by default auto.
        max_model_length : Optional[int], optional
            Maximum length of the model, by default None. If None, the maximum length will be determined from the model config.
        default_models : Optional[dict[str, str]], optional
            Default models mapping, by default None. If None, a default mapping will be used.
        use_cloud : bool, optional
            Whether to use huggingface inference API, by default False.
        huggingface_token : Optional[str], optional
            Huggingface inference API token, by default None. If None, the token will be read from the environment variable HUGGINGFACE_TOKEN.

        **kw
            Keyword arguments to pass to the translation pipeline.

        Example
        --------
        >>> from bntrans import Translator
        >>> translator = Translator(src="en", dest="bn")
        >>> translator.translate("Hello world!") #  ্যালো বিশ্ব!
        """

        self.default_models = default_models or {
            "en-bn": "shhossain/opus-mt-en-to-bn",
            "bn-en": "Helsinki-NLP/opus-mt-bn-en",
        }

        try:
            self.model = model or self.default_models[f"{src}-{dest}"]
        except KeyError:
            raise ValueError(
                f"Model not found for {src}-{dest}. Please specify a model."
            )

        self.max_model_length = max_length
        self.use_cloud = use_cloud
        token = huggingface_token or os.environ.get("HUGGINGFACE_TOKEN")
        if token is None and use_cloud:
            raise ValueError(
                "Huggingface token not found. Please specify a token or set the environment variable HUGGINGFACE_TOKEN."
            )
        self.huggingface_token: str = token  # type: ignore

        device = None
        if not use_gpu:
            device = "cpu"
        if "device" not in kw or "device_map" not in kw:
            kw["device"] = device

        self.tokenizer = AutoTokenizer.from_pretrained(self.model)
        self.config = AutoConfig.from_pretrained(self.model)
        self.kw = kw

        self._pipeline = None

    @property
    def pipeline(self):
        if self._pipeline is None:
            if self.use_cloud:
                self._pipeline = CloudPipeline(self.model, self.huggingface_token)
            else:
                self._pipeline = pipeline("translation", model=self.model, **self.kw)

        return self._pipeline

    def is_bangla(self, text: str):
        return any(0x0980 <= ord(c) <= 0x09FF for c in text)

    def get_max_length(self) -> int:
        if self.max_model_length is not None:
            return self.max_model_length

        try:
            if self.model in model_config:
                return model_config[self.model]["max_position_embeddings"]

            return self.config.max_position_embeddings

        except Exception:
            if self.max_model_length is None:
                warnings.warn(
                    "Max model length not found in config. Specify max_length in the constructor to avoid this warning."
                )

        return 128

    def generate(self, text: str, **kw) -> list[dict]:
        token_length = 1024
        try:
            input_ids = self.tokenizer(text, return_tensors="pt").input_ids
            token_length = len(input_ids[0])
        except Exception as e:
            warnings.warn("Failed to tokenize text. " + str(e))
            pass

        if token_length > self.get_max_length():
            func = sent_tokens_english
            if self.is_bangla(text):
                func = sent_tokens_bangla

            return self.pipeline(func(text), **kw)  # type: ignore

        else:
            return self.pipeline(text, **kw)  # type: ignore

    def translate(self, text: str, delimiter: str = "\n", **kw):
        """
        Translate text from source language to destination language.

        Parameters
        ----------
        text : str
            Text to translate.
        delimiter : str, optional
            Delimiter to join multiple translations, by default "\n". Only used for long texts.

        **kw
            Keyword arguments to pass to the translation pipeline.

        Returns
        -------
        str
            Translated text.


        """

        result = self.generate(text, **kw)
        if len(result) == 1:
            return result[0]["translation_text"]
        else:
            return f"{delimiter}".join([r["translation_text"] for r in result])

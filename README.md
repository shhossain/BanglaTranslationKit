# BanglaTranslationKit

BanglaTranslationKit is a collaborative open-source language translation package meticulously designed for smooth offline conversion between both Bangla and English languages (English to Bangla and Bangla to English)

## Installation

```bash
pip install bangla-translation-kit
```

## Usage

You can use this package to translate any Bangla to English or English to Bangla.

```python
from bntrans import Translator

translator = Translator(src="en", dest="bn")
translation = translator.translate("Hello world!")  #  ্যালো বিশ্ব!
print(translation)
```

### Some Useful Methods

```python
from bntrans import Translator

# You can tell the model to use cpu
translator = Translator(src="en", dest="bn", use_gpu=False)

# Specify a custom model (from huggingface.co/models or local path)
translator = Translator(model="mymodel")

# If custom model doesn't have a maximum length, you can specify it. It is better to specify it as some models have wrong maximum length in their config.
translator = Translator(model="mymodel", max_length=512)

# You can also use `generate` method to get raw output from the model
translator.generate("Hello world!")
```

## Use Cloud Translation API (Free)

If you want to test the model without installing it, you can use the cloud translation API. Get a free Token from [here](https://huggingface.co/settings/tokens) (Read Token is enough) and use it like this:

```python
from bntrans import Translator

translator = Translator(src="en", dest="bn", use_cloud=True, huggingface_token="YOUR_TOKEN")
translation = translator.translate("Hello world!")  #  ্যালো বিশ্ব!
print(translation)
```

## Use in Command Line

You can also use this package in command line. Just install it and run the following command:

```bash
bntrans "Hello world!"
```

```bash
usage: cli.py [-h] [-s SRC] [-d DEST] [-m MODEL] [-g GPU] [-l MAX_LENGTH] [-c USE_CLOUD] [-t HUGGINGFACE_TOKEN] text

Translate text from one language to another.

positional arguments:
  text                  Text to translate

options:
  -h, --help            show this help message and exit
  -s SRC, --src SRC     Source language (default: en)
  -d DEST, --dest DEST  Destination language (default: bn)
  -m MODEL, --model MODEL
                        Model to use for translation
  -g GPU, --gpu GPU     Whether to use GPU for translation (default: True)
  -l MAX_LENGTH, --max-length MAX_LENGTH
                        Maximum length of the model (default: None)
  -c USE_CLOUD, --use-cloud USE_CLOUD
                        Whether to use huggingface inference API (default: False)
  -t HUGGINGFACE_TOKEN, --huggingface-token HUGGINGFACE_TOKEN
                        Huggingface inference API token (default: None)
```

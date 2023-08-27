from bntrans import Translator


translator = Translator(src="bn", dest="en", use_cloud=True, huggingface_token="YOUR_TOKEN_HERE")

while True:
    text = input("Enter text: ")
    print(translator.translate(text))

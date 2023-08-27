from bntrans import Translator


translator = Translator(src="en", dest="bn", use_cloud=True, huggingface_token="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")

while True:
    text = input("Enter text: ")
    print(translator.translate(text))

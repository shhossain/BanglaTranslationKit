import argparse
import os

# text (str or path): Text to translate or --interactive flag
# -s --src (str): Source language (default: en)
# -d --dest (str): Destination language (default: bn)
# -m --model (str): Model to use for translation
# -g --gpu (bool): Whether to use GPU for translation (default: True)
# -l --max-length (int): Maximum length of the model (default: None)
# -c --use-cloud (bool): Whether to use huggingface inference API (default: False)
# -t --huggingface-token (str): Huggingface inference API token (default: None)


def main():
    parser = argparse.ArgumentParser(
        description="Translate text from one language to another."
    )
    parser.add_argument("text", type=str, help="Text to translate")
    parser.add_argument(
        "-s", "--src", type=str, default="en", help="Source language (default: en)"
    )
    parser.add_argument(
        "-d",
        "--dest",
        type=str,
        default="bn",
        help="Destination language (default: bn)",
    )
    parser.add_argument(
        "-m", "--model", type=str, default=None, help="Model to use for translation"
    )
    parser.add_argument(
        "-g",
        "--gpu",
        type=bool,
        default=True,
        help="Whether to use GPU for translation (default: True)",
    )
    parser.add_argument(
        "-l",
        "--max-length",
        type=int,
        default=None,
        help="Maximum length of the model (default: None)",
    )
    parser.add_argument(
        "-c",
        "--use-cloud",
        type=bool,
        default=False,
        help="Whether to use huggingface inference API (default: False)",
    )
    parser.add_argument(
        "-t",
        "--huggingface-token",
        type=str,
        default=None,
        help="Huggingface inference API token (default: None)",
    )

    args = parser.parse_args()
    
    from bntrans import Translator
    
    translator = Translator(
        src=args.src,
        dest=args.dest,
        model=args.model,
        use_gpu=args.gpu,
        max_length=args.max_length,
        use_cloud=args.use_cloud,
        huggingface_token=args.huggingface_token,
    )

    text = args.text
    if os.path.isfile(text):
        with open(text, "r", encoding="utf-8") as f:
            text = f.read()

    print(translator.translate(text))


if __name__ == "__main__":
    main()
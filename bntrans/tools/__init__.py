import pysbd

segen = pysbd.Segmenter(language="en", clean=False)
segbn = pysbd.Segmenter(language="bn", clean=False)


def sent_tokens_english(text):
    return segen.segment(text)

def sent_tokens_bangla(text):
    return segbn.segment(text)
    
    
    

    
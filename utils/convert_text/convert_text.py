import os
import os 
from pdfminer.high_level import extract_pages, extract_text
from tqdm.contrib import tzip
import signal
import sys

def extract_text_f(pdf, txt, large_files, max_file_size):
    with open(pdf, "rb") as f:
        # if we check only small files
        if not large_files:
            # get size
            stats = os.stat(pdf)
            size = stats.st_size / (1024 * 1024)
            # if size > max_size, return
            if size > max_file_size:
                return
        
        try:
            text = extract_text(f)
        except BaseException as e:
            return
        
        with open(txt, "w") as t:
                t.write(text)
        
        return 
    
def handle_sigint(sig, frame):
    print('SIGINT received, terminating.')
    sys.exit()


def handle_timeout(sig, frame):
    raise TimeoutError('took too long')


def get_texts_from_pdf(signal_alarm=10, max_file_size=200, large_files=True):
    signal.signal(signal.SIGINT, handle_sigint)
    signal.signal(signal.SIGALRM, handle_timeout)
    pdfs = [f"./klimaatadaptatie/pdf/{i}" for i in os.listdir("./klimaatadaptatie/pdf/")]
    txts = [pdf.replace("pdf/", "txt/").replace(".pdf", ".txt") for pdf in pdfs]
    already_txts = [f"./klimaatadaptatie/txt/{i}" for i in os.listdir("./klimaatadaptatie/txt/")]

    if large_files:
        print("Checking large files as well")
    else:
        print(f"Large files disabled, checking up to n{max_file_size} mb")

    for pdf, txt in tzip(pdfs, txts): 
        if txt not in already_txts:
            try:
                signal.alarm(signal_alarm)
                _ = extract_text_f(pdf, txt, large_files, max_file_size)
            except TimeoutError as exc:
                print('{}: {}'.format(exc.__class__.__name__, exc))

    return True

if __name__ == "__main__":
    print(" Start!")
    _ = get_texts_from_pdf()

    
import os
import re

import fitz
import requests
from dotenv import load_dotenv

load_dotenv()

PRODUCTION_ENDPOINT = "https://asimov-legalai--longformer-test-model-parse.modal.run"
DEV_ENDPOINT = "https://asimov-legalai--longformer-test-model-parse-dev.modal.run"


def read_pdf(pdf_path):
    fitz_doc = fitz.open(pdf_path)
    text = "\n".join(
        [f"Pag. {i+1}\n\n{page.get_text()}" for i, page in enumerate(fitz_doc)]
    )
    return re.sub("\n+", "\n", text)


data = {"text": read_pdf("fascicoli/AC1632.pdf"), "api_key": os.environ["MODAL_KEY"]}
response = requests.post(
    DEV_ENDPOINT,  # Alternatively, PRODUCTION_ENDPOINT
    json=data,
)
print(response.json())

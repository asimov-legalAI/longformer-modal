import os

import modal

from longformer_modal.models import ParseArgument
from longformer_modal.parser import AmendmentsParserSenatoAI

_CURRENT_DIR = os.path.dirname(__file__)

GPU_CONFIG = modal.gpu.Any(count=1)


app = modal.App(name="longformer-test")

image = modal.Image.debian_slim(python_version="3.10").pip_install(
    "transformers==4.39.3", "torch==2.3.1", "fastapi==0.111.0"
)


@app.cls(
    gpu=GPU_CONFIG,
    image=image,
    timeout=60 * 10,
    container_idle_timeout=60 * 10,
    allow_concurrent_inputs=10,
)
class Model:
    @modal.enter()
    def setup(self):
        from dotenv import load_dotenv

        load_dotenv(os.path.join(_CURRENT_DIR, ".env"))

        self.parser = AmendmentsParserSenatoAI(
            model_path=os.path.join(_CURRENT_DIR, "EC_0611_A_ckp"), device="cuda"
        )

    @modal.web_endpoint(method="POST")
    def parse(self, parse_argument: ParseArgument):
        from fastapi import HTTPException

        if parse_argument.api_key != os.environ["API_KEY"]:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials",
            )
        return {"amendments": self.parser.parse(parse_argument.text)}

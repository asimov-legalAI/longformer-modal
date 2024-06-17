# Longformer - Modal

First, set up a virtual environment and install all of the required dependencies, either using `poetry` and `pyproject.toml` or `pip` and `requirements.txt`. Importantly, be sure to add our `EC_0611_A_ckp` model to the `longformer_modal` folder.

## Serve the endpoint in dev mode

To serve the parsing endpoint on [modal.com](http://modal.com) in dev mode, run  `modal serve longformer_modal.app`. You can check the app status on modal website by logging in as `asimov-legalai`, using the same password we use to access info emails.

## Deploy the endpoint

To persistently deploy the endpoint, run `modal deploy longformer_modal.app`. You can check the deployment status on modal website by logging in as `asimov-legalai`, using the same password we use to access info emails.

## Examples

To start developing, or test the deployment, run:
```
cd examples
python run.py
```
The script default is dev mode. If you want to change the mode to production, just replace the request endpoint in the script.

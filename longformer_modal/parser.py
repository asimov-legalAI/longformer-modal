BEGIN_AMENDMENT_LABEL = 1


def chunk_tokenizer_output(encodings, chunk_size):
    from transformers import BatchEncoding

    input_ids = encodings["input_ids"]
    attention_mask = encodings["attention_mask"]
    labels = encodings.get("labels")
    return [
        BatchEncoding(
            dict(
                input_ids=input_ids[i : i + chunk_size],
                attention_mask=attention_mask[i : i + chunk_size],
                **{"labels": labels[i : i + chunk_size]} if labels is not None else {},
            )
        )
        for i in range(0, len(input_ids), chunk_size)
    ]


class AmendmentsParserSenatoAI:
    def __init__(self, model_path, device="cpu"):
        from transformers import AutoModelForTokenClassification, AutoTokenizer

        self.model = AutoModelForTokenClassification.from_pretrained(model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.device = device

    def forward(self, tokenizer_outputs):
        import torch

        input_ids = (
            torch.Tensor(tokenizer_outputs["input_ids"])
            .int()
            .reshape(1, -1)
            .to(self.device)
        )
        attention_mask = (
            torch.Tensor(tokenizer_outputs["attention_mask"])
            .int()
            .reshape(1, -1)
            .to(self.device)
        )
        self.model.to(self.device)
        with torch.no_grad():
            return self.model(input_ids, attention_mask).logits

    def predict(self, tokenizer_outputs):
        logits = self.forward(tokenizer_outputs)
        return torch.argmax(logits, dim=-1).squeeze().tolist()

    def __call__(self, tokenizer_outputs):
        return self.predict(tokenizer_outputs)

    def _extract_amendments(self, input_ids, predictions):
        amendments_ends = [
            i for i, j in enumerate(predictions) if j == BEGIN_AMENDMENT_LABEL
        ]
        amendments_ends.append(None)
        amendments_tokens = [
            input_ids[i:j] for i, j in zip(amendments_ends, amendments_ends[1:])
        ]
        return [
            self.tokenizer.decode(amendment_tokens)
            for amendment_tokens in amendments_tokens
        ]

    def parse(self, text):
        encodings = self.tokenizer(text, add_special_tokens=False)
        chunked_encodings = chunk_tokenizer_output(encodings, chunk_size=4000)
        predictions = []
        for chunked_encoding in chunked_encodings:
            predictions.extend(self.predict(chunked_encoding))
        return self._extract_amendments(encodings["input_ids"], predictions)

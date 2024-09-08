from transformers import T5ForConditionalGeneration, T5Tokenizer


def predict_cast(keywords: str, model: T5ForConditionalGeneration, tokenizer: T5Tokenizer):
    # Tokenize the input keywords
    inputs = tokenizer(
        keywords, max_length=max_length, truncation=True, padding="max_length", return_tensors="pt"
    ).input_ids

    # Generate the output cast using the model
    generated_ids = model.generate(inputs, max_length=max_length, num_beams=5, early_stopping=True)

    # Decode the generated output into text
    cast = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    return cast


if __name__ == "__main__":
    model_path = "/home/ubuntu/hackathon6/transformers_models/models_cast/checkpoint-2502"

    model = T5ForConditionalGeneration.from_pretrained(model_path)
    tokenizer = T5Tokenizer.from_pretrained(model_path, legacy=False)
    max_length = 300
    while True:
        keywords = input("Enter keywords: ")
        predicted_cast = predict_cast(keywords, model, tokenizer)
        print(predicted_cast)

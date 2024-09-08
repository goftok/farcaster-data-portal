import torch
import random
import pandas as pd
import wandb
from transformers import T5ForConditionalGeneration, T5Tokenizer
from transformers import Seq2SeqTrainer, Seq2SeqTrainingArguments
from sklearn.model_selection import train_test_split
from utils.console import console

model_name = "google/flan-t5-base"
dataset_path = "/home/ubuntu/hackathon6/data/100k_filtered_casts_and_keywords.xlsx"
output_dir = "/home/ubuntu/hackathon6/transformers_models/models_cast"
max_length = 300

model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name, legacy=False)

df = pd.read_excel(dataset_path, engine="openpyxl")
df = df.dropna()

train_df, eval_df = train_test_split(df, test_size=0.3, random_state=42)


# Function to tokenize the dataset
def tokenize_data(df, tokenizer: T5Tokenizer):
    inputs = df["Keywords"].tolist()
    outputs = df["Casts"].tolist()

    # Tokenize inputs (keywords) and outputs (casts)
    tokenized_inputs = tokenizer(
        inputs, max_length=max_length, truncation=True, padding="max_length", return_tensors="pt"
    )
    tokenized_outputs = tokenizer(
        outputs, max_length=max_length, truncation=True, padding="max_length", return_tensors="pt"
    )

    # The output labels must be formatted as decoder input IDs, so we shift them
    labels = tokenized_outputs["input_ids"]

    # Replace padding token ID in the labels with -100 so that they are ignored by the loss function
    labels[labels == tokenizer.pad_token_id] = -100

    return {
        "input_ids": tokenized_inputs["input_ids"],
        "attention_mask": tokenized_inputs["attention_mask"],
        "labels": labels,
    }


tokenized_train_dataset = tokenize_data(train_df, tokenizer)
tokenized_eval_dataset = tokenize_data(eval_df, tokenizer)


class CustomDataset(torch.utils.data.Dataset):
    def __init__(self, encodings):
        self.encodings = encodings

    def __getitem__(self, idx):
        return {key: val[idx] for key, val in self.encodings.items()}

    def __len__(self):
        return len(self.encodings["input_ids"])


train_dataset = CustomDataset(tokenized_train_dataset)
eval_dataset = CustomDataset(tokenized_eval_dataset)

# get random sample
random_idx = random.randint(0, len(train_dataset))
sample_input = train_dataset[random_idx]["input_ids"]
sample_output = train_dataset[random_idx]["labels"]
filtered_sample_output = sample_output[sample_output != -100]
sample_attention_mask = train_dataset[random_idx]["attention_mask"]


console.print("\nEncoded input (token IDs):")
console.print(sample_input)

console.print("\n Decoded input:")
console.print(tokenizer.decode(sample_input, skip_special_tokens=True))

console.print("\nEncoded output (token IDs):")
console.print(sample_output)

console.print("\n Decoded output:")
console.print(tokenizer.decode(filtered_sample_output, skip_special_tokens=True))  # Remove -100 tokens

console.print("\nAttention mask:")
console.print(sample_attention_mask)

console.print("\n Training dataset length:")
console.print(len(train_dataset))

console.print("\n Evaluation dataset length:")
console.print(len(eval_dataset))


training_args = Seq2SeqTrainingArguments(
    output_dir=output_dir,
    eval_strategy="epoch",
    save_strategy="epoch",
    learning_rate=9e-5,
    fp16=False,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=16,
    weight_decay=0.01,
    save_total_limit=2,
    num_train_epochs=10,
    predict_with_generate=True,
)


trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer,
)

project = "hackathon_cast"
wandb.login()
wandb.init(name="t5_v3", project=project, reinit=True)

trainer.train()

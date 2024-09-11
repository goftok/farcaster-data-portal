import os
import torch
import random
import wandb
import pandas as pd
from dotenv import load_dotenv

from transformers import T5ForConditionalGeneration, T5Tokenizer
from transformers import Seq2SeqTrainer, Seq2SeqTrainingArguments
from transformers import EvalPrediction
from sklearn.model_selection import train_test_split
from utils.console import console
from evaluate import load

load_dotenv()

model_name = "google/flan-t5-base"
dataset_path = os.getenv("DATASET_PATH")
output_dir = os.getenv("MODEL_OUTPUT_DIR")
max_length = 250
test_size = 0.2
seed = 14

# Load the BLEU and ROUGE metrics
bleu_metric = load("bleu")
rouge_metric = load("rouge")

console.print(f"Dataset path: {dataset_path}")
console.print(f"Output directory: {output_dir}")
if not dataset_path or not output_dir or not os.path.exists(dataset_path) or not os.path.exists(output_dir):
    raise ValueError("Please set the DATASET_PATH and MODEL_OUTPUT_DIR environment variables")

model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name, legacy=False)

df = pd.read_excel(dataset_path, engine="openpyxl")
df = df.dropna()
# if df.isna().sum().sum() > 0:
#     raise ValueError("Dataset contains missing values")

train_df, eval_df = train_test_split(df, test_size=test_size, random_state=seed)


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


def compute_metrics(pred: EvalPrediction):
    # Decode generated predictions and reference labels
    labels_ids = pred.label_ids
    pred_ids = pred.predictions

    # Replace padding token ids (-100) with the pad token for labels
    pred_str = tokenizer.batch_decode(pred_ids, skip_special_tokens=True)
    labels_ids[labels_ids == -100] = tokenizer.pad_token_id
    label_str = tokenizer.batch_decode(labels_ids, skip_special_tokens=True)

    # Compute BLEU score
    bleu = bleu_metric.compute(predictions=[pred_str], references=[label_str])

    # Compute ROUGE score
    rouge = rouge_metric.compute(predictions=pred_str, references=label_str, use_stemmer=True)

    # Return the BLEU and ROUGE metrics
    return {
        "bleu": bleu["bleu"],
        "rouge1": rouge["rouge1"].mid.fmeasure,
        "rouge2": rouge["rouge2"].mid.fmeasure,
        "rougeL": rouge["rougeL"].mid.fmeasure,
    }


training_args = Seq2SeqTrainingArguments(
    output_dir=output_dir,
    eval_strategy="epoch",
    save_strategy="epoch",
    learning_rate=5e-5,
    fp16=False,
    weight_decay=0.01,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=6,
    gradient_accumulation_steps=2,
    save_total_limit=2,
    num_train_epochs=10,
    predict_with_generate=True,
    metric_for_best_model="bleu",
)


trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

project = "hackathon_cast"
wandb.login()
wandb.init(name="t5_v4", project=project, reinit=True)

trainer.train()

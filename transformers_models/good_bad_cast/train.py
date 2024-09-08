import wandb
import numpy as np

from transformers import Trainer, TrainingArguments, DataCollatorWithPadding
from transformers import BertForSequenceClassification, BertTokenizer
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

from utils.console import console
from db_connection import conn
from transformers_models.good_bad_cast.dataset import RegressionDataset
from transformers_models.good_bad_cast.dataset import create_dataset, check_data

# from transformers_models.utils import compute_average_input_length


base_model = "google-bert/bert-base-uncased"
output_dir = "/home/ubuntu/hackathon6/transformers_models/models"
max_length = 250

model = BertForSequenceClassification.from_pretrained(base_model, num_labels=1)
tokenizer = BertTokenizer.from_pretrained(base_model, clean_up_tokenization_spaces=True)
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)


def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.squeeze(predictions)

    # Compute R2 score
    r2 = r2_score(labels, predictions)

    # Compute Mean Squared Error (MSE)
    mse = mean_squared_error(labels, predictions)

    # Compute Mean Absolute Error (MAE)
    mae = mean_absolute_error(labels, predictions)

    return {
        "r2": r2,
        "mse": mse,
        "mae": mae,
    }


train_df, test_df, mean, std = create_dataset(conn)

train_encodings = tokenizer(train_df["text"].tolist(), padding=True, truncation=True, max_length=250)
test_encodings = tokenizer(test_df["text"].tolist(), padding=True, truncation=True, max_length=250)

train_dataset = RegressionDataset(train_encodings, train_df["labels"].tolist())
test_dataset = RegressionDataset(test_encodings, test_df["labels"].tolist())


training_args = TrainingArguments(
    output_dir=output_dir,
    do_train=True,
    learning_rate=5e-5,
    per_device_train_batch_size=85,
    per_device_eval_batch_size=85,
    # auto_find_batch_size=True,
    num_train_epochs=20,
    weight_decay=0.01,
    fp16=False,
    eval_strategy="epoch",
    save_strategy="epoch",
    save_total_limit=2,
    load_best_model_at_end=True,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

check_data(train_dataset, tokenizer, std, mean)

# train_avg_length = compute_average_input_length(train_dataset, tokenizer)
# test_avg_length = compute_average_input_length(test_dataset, tokenizer)

# print(f"Average input length for training dataset: {train_avg_length}")
# print(f"Average input length for test dataset: {test_avg_length}")

console.print(f"Training dataset size: {len(train_df)}")
console.print(f"Test dataset size: {len(test_df)}")
console.print(f"Tokenizer vocab size: {len(trainer.tokenizer.get_vocab())}")

project = "hackathon"
wandb.login()
wandb.init(name="bert_v1", project=project, reinit=True)

trainer.train()

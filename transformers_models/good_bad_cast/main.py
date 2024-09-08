import numpy as np

from transformers import Trainer, TrainingArguments
from transformers import BertForSequenceClassification, BertTokenizer
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

from db_connection import conn


base_model = "google-bert/bert-base-uncased"

model = BertForSequenceClassification.from_pretrained(base_model, num_labels=1)


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

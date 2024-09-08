from transformers import PreTrainedTokenizer
from transformers_models.good_bad_cast.dataset import RegressionDataset


def compute_average_input_length(dataset: RegressionDataset, tokenizer: PreTrainedTokenizer) -> float:
    total_length = 0
    num_samples = len(dataset)

    # Get the special token IDs (such as padding tokens) from the tokenizer
    special_token_ids = {
        tokenizer.pad_token_id,
        tokenizer.cls_token_id,
        tokenizer.sep_token_id,
    }

    for i in range(num_samples):
        input_ids = dataset[i]["input_ids"]

        # Exclude special tokens from the input length calculation
        input_length = len([token_id for token_id in input_ids if token_id not in special_token_ids])

        total_length += input_length

    # Compute the average input length
    average_length = total_length / num_samples
    return average_length

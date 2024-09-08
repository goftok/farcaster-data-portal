from transformers_models.good_bad_cast.dataset import RegressionDataset


def compute_average_input_length(dataset: RegressionDataset) -> float:
    total_length = 0
    num_samples = len(dataset)

    for i in range(num_samples):
        input_length = len(dataset[i]["input_ids"])
        total_length += input_length

    average_length = total_length / num_samples
    return average_length

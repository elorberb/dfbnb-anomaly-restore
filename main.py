# main.py
from experiment_utils import run_experiments


def main():
    # Expanded configurations for both normal and anomaly conditions
    configurations = [
        {"branching_factors": [3, 4, 5, 6, 7, 8], "depths": [6, 8, 10], "file_prefix": "normal_conditions",
         "edge_cost_distribution": "uniform"},
        {"branching_factors": [3, 4, 5, 6, 7, 8], "depths": [6, 8, 10], "file_prefix": "anomaly_conditions",
         "edge_cost_distribution": "zero_or_one"},
        {"branching_factors": [5, 6, 7, 8], "depths": [10, 12, 14], "file_prefix": "normal_conditions_high",
         "edge_cost_distribution": "uniform"},
        {"branching_factors": [5, 6, 7, 8], "depths": [10, 12, 14], "file_prefix": "anomaly_conditions_high",
         "edge_cost_distribution": "zero_or_one"}
    ]

    num_repetitions = 10
    db_dir = 'databases'
    output_dir = 'results'
    verbose = False

    for config in configurations:
        df = run_experiments(
            branching_factors=config["branching_factors"],
            depths=config["depths"],
            num_repetitions=num_repetitions,
            db_dir=db_dir,
            output_dir=output_dir,
            file_prefix=config["file_prefix"],
            verbose=verbose,
            edge_cost_distribution=config["edge_cost_distribution"],
        )
        print(df)


if __name__ == "__main__":
    main()

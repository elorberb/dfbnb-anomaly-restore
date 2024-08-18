# main.py
from experiment_utils import run_experiments
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Expanded configurations for both normal and anomaly conditions
    configurations = [
        {"branching_factors": [2, 3], "depths": range(2, 21), "file_prefix": "normal_conditions",
        "edge_cost_distribution": "uniform"},
        {"branching_factors": [2, 3], "depths": range(2, 21), "file_prefix": "anomaly_conditions",
        "edge_cost_distribution": "zero_or_one"},
        {"branching_factors": [4, 5], "depths": range(2, 21), "file_prefix": "normal_conditions_high_branching_factor",
        "edge_cost_distribution": "uniform"},
        {"branching_factors": [4, 5], "depths": range(2, 21), "file_prefix": "anomaly_conditions_high_branching_factor",
        "edge_cost_distribution": "zero_or_one"},
    ]

    num_repetitions = 10
    db_dir = 'databases'
    output_dir = 'results'
    verbose = False

    for config in configurations:
        logger.info(f"Running experiments for {config['file_prefix']}...")
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

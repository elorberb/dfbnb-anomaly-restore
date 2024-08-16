import os
import pandas as pd
from dfbnb import DFBnB


def run_experiments(branching_factors, depths, num_repetitions=12, db_dir='databases', output_dir='results',
                    file_prefix='experiment', verbose=False, edge_cost_distribution="zero_or_one"):
    """Runs the Depth-First Branch-and-Bound experiments across various branching factors and depths.

    Parameters:
    - branching_factors: List or range of branching factors to test.
    - depths: List or range of depths to test.
    - num_repetitions: Number of repetitions for averaging the results.
    - db_dir: Directory where the database files will be stored.
    - output_dir: Directory where the output CSV files will be saved.
    - file_prefix: Prefix for the output CSV file names.
    - verbose: Boolean flag to enable verbose output during search.
    - edge_cost_distribution: String to specify the distribution of edge costs ("zero_or_one", "uniform", "custom").
    """

    # Ensure output directories exist
    os.makedirs(db_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # DataFrame to hold results
    results_df = pd.DataFrame(index=branching_factors, columns=depths)
    print('--- Starting the Experiment ---')
    print(f"Running with Depth range: {depths} and Branching factors: {branching_factors}")

    for depth in depths:
        print(f'------ Depth: {depth} ------')
        for branching_factor in branching_factors:
            try:
                print(f'--------------------- Branching Factor: {branching_factor} ---------------------')
                total_nodes_expanded = 0

                for _ in range(num_repetitions):
                    # Create unique database file path for each experiment
                    db_file = os.path.join(db_dir, f'{file_prefix}_graph_b{branching_factor}_d{depth}.db')
                    dfbnb = DFBnB(branching_factor=branching_factor, depth=depth, db_path=db_file,
                                  verbose=verbose, edge_cost_distribution=edge_cost_distribution)

                    _, expanded_nodes = dfbnb.depth_first_search_with_pruning()
                    total_nodes_expanded += len(expanded_nodes)

                # Store the average result
                results_df.at[branching_factor, depth] = total_nodes_expanded / num_repetitions

            except Exception as e:
                print(f"An error occurred: {e}")
                # Save the results so far in case of an error
                save_results(results_df, output_dir, file_prefix)
                return results_df

        # Save results after each depth iteration
        save_results(results_df, output_dir, file_prefix)
        print("--- Finished ---")

    # Final save of results
    save_results(results_df, output_dir, file_prefix)
    return results_df


def save_results(results_df, output_dir, file_prefix):
    """Saves the results DataFrame to a CSV file."""
    output_file = os.path.join(output_dir, f'{file_prefix}_results.csv')
    results_df.to_csv(output_file)
    print(f"Results saved to {output_file}")

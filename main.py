# main.py
from experiment_utils import run_experiments


def main():
    branching_factors = range(3, 8)
    depths = range(2, 5)
    num_repetitions = 20
    verbose = True
    df = run_experiments(branching_factors=branching_factors,
                         depths=depths,
                         num_repetitions=num_repetitions,
                         verbose=verbose)
    print(df)


if __name__ == "__main__":
    main()

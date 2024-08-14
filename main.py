# main.py
from experiment_utils import run_experiments


def main():
    branching_factors = range(6, 8)
    depths = range(2, 5)

    df = run_experiments(branching_factors=branching_factors, depths=depths)
    print(df)


if __name__ == "__main__":
    main()

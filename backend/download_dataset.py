"""
TruthLens - Dataset Preparation Script

Creates:
    dataset.csv

from:
    Fake.csv
    True.csv
"""

import os
import pandas as pd

DATA_DIR = os.path.join(
    os.path.dirname(__file__),
    'data'
)

FAKE_PATH = os.path.join(DATA_DIR, 'Fake.csv')

TRUE_PATH = os.path.join(DATA_DIR, 'True.csv')

OUTPUT_PATH = os.path.join(DATA_DIR, 'dataset.csv')


def main():

    print("=" * 60)
    print(" TruthLens - Dataset Preparation")
    print("=" * 60)

    # Check files
    if not os.path.exists(FAKE_PATH):

        print("Fake.csv not found!")
        return

    if not os.path.exists(TRUE_PATH):

        print("True.csv not found!")
        return

    print("Loading datasets...")

    fake_df = pd.read_csv(FAKE_PATH)

    true_df = pd.read_csv(TRUE_PATH)

    # Add labels
    fake_df['label'] = 1

    true_df['label'] = 0

    # Combine
    dataset = pd.concat(
        [fake_df, true_df],
        ignore_index=True
    )

    # Shuffle
    dataset = dataset.sample(
        frac=1,
        random_state=42
    ).reset_index(drop=True)

    # Save
    dataset.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(f"Dataset created successfully!")

    print(f"Saved to:")
    print(OUTPUT_PATH)

    print(f"\nTotal samples: {len(dataset)}")

    print(
        f"Fake: {len(dataset[dataset.label == 1])}"
    )

    print(
        f"Real: {len(dataset[dataset.label == 0])}"
    )

    print("=" * 60)


if __name__ == '__main__':
    main()
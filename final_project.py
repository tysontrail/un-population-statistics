# final_project.py
#
# Group name:
# - Kernel Panic
#
# Team members:
# - Tyson Trail
# - Kevin Amado
#

# Third party libraries
from typing import List
import pandas as pd
import numpy as np


def main() -> None:

    # Stage 2: DataFrame Creation

    data: pd.DataFrame = load_and_merge_data()

    print(data)

    # Stage 3: User Entry

    # Prompt User to Select Country
    while True:
        try:
            country_or_area: str = input("Please enter a Country or Area: ")

            valid_countries_or_areas: List[str] = data.index.levels[0]

            if country_or_area in valid_countries_or_areas:
                break
            else:
                raise ValueError
        except ValueError:
            print("You must enter a valid Country or Area.\n")

    # Create sub dataframe for country
    country_data = data.loc[country_or_area, :]
    print()
    print(country_data)

    # Prompt User to Select Year
    while True:
        try:
            year: int = int(input("Please choose from available Years: "))

            if year in country_data.index:
                break
            else:
                raise ValueError
        except ValueError:
            print("Please choose from the available Years.")

    print()
    # Print data for chosen country and year
    print(country_data.loc[year])
    print()

    # Stage 4: Analyis and Calculations

    # Add additional columns to the dataset
    # data["Life expectancy at birth for both sexes (years)"]
    print("Aggregate Stats for the Dataset")
    print(data.describe().T)
    print()

    # Stage 5: Export and Matplotlib
    data.to_excel("data.xlsx")


def load_and_merge_data() -> pd.DataFrame:
    population_1: pd.DataFrame = pd.read_excel(
        "UN Population Datasets/UN Population Dataset 1.xlsx",
        usecols=["M49 Code", "Year", "Region/Country/Area", "Series", "Value"],
    )
    population_2: pd.DataFrame = pd.read_excel(
        "UN Population Datasets/UN Population Dataset 2.xlsx",
        usecols=["M49 Code", "Year", "Region/Country/Area", "Series", "Value"],
    )
    population: pd.DataFrame = (
        pd.merge(population_1, population_2, how="outer")
        .set_index(["M49 Code", "Year"])
        .pivot(columns=["Series"], values="Value")
        .reset_index()
    )
    m49: pd.DataFrame = pd.read_excel(
        "UN Population Datasets/UN M49.xlsx",
        usecols=[
            "M49 Code",
            "Global Name",
            "Region Name",
            "Sub-region Name",
            "Country or Area",
            "ISO-alpha2 Code",
            "ISO-alpha3 Code",
        ],
    )

    data: pd.DataFrame = (
        pd.merge(m49, population, how="inner", on=["M49 Code"])
        .set_index(["Country or Area", "Year"])
        .sort_index()
        .dropna()
    )

    return data


if __name__ == "__main__":
    main()

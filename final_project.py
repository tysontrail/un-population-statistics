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
            country_or_area = input("Please enter a Country or Area: ")

            if country_or_area in data.index.levels[0]:
                # Create sub dataframe for country
                sub_data = data.loc[country_or_area, :]
                print()
                print(sub_data)
                break
            else:
                raise ValueError
        except ValueError:
            print("You must enter a valid Country or Area.\n")

    # Prompt User to Select Year
    while True:
        try:
            year = int(input("Please choose from available Years: "))

            if year in sub_data.index:
                print()
                # Print data for chosen country and year
                print(sub_data.loc[year])
                print()
                break
            else:
                raise ValueError
        except ValueError:
            print("Please choose from the available Years.")

    # Stage 4: Analyis and Calculations
    print("Aggregate Stats for the Dataset")
    print(data.describe())
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

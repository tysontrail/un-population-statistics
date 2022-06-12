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
import pandas as pd  # Tested with pandas==1.4.2
# Standard library
import textwrap
from typing import (
    Any,
    List,
    Tuple,
)


def main() -> None:
    # Stage 2: DataFrame Creation
    data: pd.DataFrame = load_and_merge_data()

    # Add additional columns to the dataset
    add_life_expectancy_column(data)
    add_fertility_rate_column(data)

    print_complete_dataset(data)

    # Stage 3: User Entry
    country: str = get_country(data)
    country_data = data.loc[country, :]
    years: Tuple[int, ...] = tuple(country_data.index)
    years_str: str = ", ".join(map(str, years))
    print_available_years_for_country(years_str)
    year: int = get_year(country_data)

    # Stage 4: Analysis and Calculations
    print_data_for_country_and_year(country, country_data, year)
    print_mean_for_all_years_for_country(country, country_data, years_str)
    print_stats_for_all_years_all_countries(data)
    print_fastest_growing_countries(data)
    print_countries_with_life_expectancy_over_80(data)

    # Matplotlib
    # TO DO

    # Stage 5: Export and Matplotlib
    export_as_xlsx(data)


def load_and_merge_data() -> pd.DataFrame:
    # Import your chosen data into a Pandas DataFrames.
    population_1: pd.DataFrame = pd.read_excel(
        "UN Population Datasets/UN Population Dataset 1.xlsx",
        usecols=["M49 Code", "Year", "Region/Country/Area", "Series", "Value"],
    )
    population_2: pd.DataFrame = pd.read_excel(
        "UN Population Datasets/UN Population Dataset 2.xlsx",
        usecols=["M49 Code", "Year", "Region/Country/Area", "Series", "Value"],
    )
    # You must use at least two merge/join operations
    # and you must delete any duplicated columns/rows
    # that result from the merge.
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
        # You must create a hierarchical index
        # of at least two levels (row or column).
        .set_index(["Country or Area", "Year"])
        # All data should be presented in the correctly sorted order,
        # depending on the index.
        .sort_index()
        # Remember to check for null values or data mismatches.
        .dropna()
    )

    return data


def add_life_expectancy_column(data: pd.DataFrame) -> None:
    data["Life expectancy difference (years) from mean"] = (
        data["Life expectancy at birth for both sexes (years)"]
        - data["Life expectancy at birth for both sexes (years)"].mean()
    )


def add_fertility_rate_column(data: pd.DataFrame) -> None:
    data["Total fertility rate (children per woman) from mean"] = (
        data["Total fertility rate (children per women)"]
        - data["Total fertility rate (children per women)"].mean()
    )


def get_country(data: pd.DataFrame) -> str:
    # Prompt User to Select Country
    while True:
        try:
            country: str = input("Please enter a Country or Area: ")

            valid_countries_or_areas: List[str] = data.index.levels[0]

            if country in valid_countries_or_areas:
                break
            else:
                raise ValueError
        except ValueError:
            print("You must enter a valid Country or Area.\n")

    return country


def get_year(country_data: pd.DataFrame) -> int:
    # Prompt User to Select Year
    while True:
        try:
            year: int = int(
                input(
                    "Please choose one of the years above "
                    "in order to display more stats: "
                )
            )

            if year in country_data.index:
                break
            else:
                raise ValueError
        except ValueError:
            print(
                "[ERROR] Invalid year. "
                "Please choose a year from the ones displayed above."
            )
    print()

    return year


def print_indented(obj: Any) -> None:
    output: str = textwrap.indent(str(obj), prefix="    ")
    print(output)


def print_complete_dataset(data: pd.DataFrame) -> None:
    print("---")
    print("Complete dataset:")
    print()
    print_indented(data)
    print()


def print_available_years_for_country(years_str: str) -> None:
    print("---")
    print("Available Years:")
    print()
    print_indented(years_str)
    print()


def print_data_for_country_and_year(
    country: str,
    country_data: pd.DataFrame,
    year: int,
) -> None:
    print("---")
    print(f"Data available for {country}, year {year}:")
    print()
    print_indented(country_data.loc[year])
    print()


def print_mean_for_all_years_for_country(
    country: str,
    country_data: pd.DataFrame,
    years_str: str,
) -> None:
    print("---")
    print(f"Aggregate mean for years: {years_str}, for {country}:")
    print()
    print_indented(country_data.mean(numeric_only=True))
    print()


def print_stats_for_all_years_all_countries(data: pd.DataFrame) -> None:
    # Use of .describe() method for combined dataset
    print("---")
    print("Aggregate stats for all years and all countries:")
    print()
    print_indented(data.describe().T)
    print()


def print_fastest_growing_countries(data: pd.DataFrame) -> None:
    # Use of groupby() method
    print("---")
    print(
        "Fastest growing countries "
        "by average annual rate of increase (percent):"
    )
    print()
    print_indented(
        data.groupby(
            "Country or Area",
        )["Population annual rate of increase (percent)"]
        .mean()
        .sort_values(ascending=False)
    )
    print()


def print_countries_with_life_expectancy_over_80(data: pd.DataFrame) -> None:
    # Use masking operation
    print("---")
    print("Countries with life expectancy over 80 years:")
    print()
    life_expectancy = data["Life expectancy at birth for both sexes (years)"]
    greater_than_80 = life_expectancy > 80
    print_indented(life_expectancy[greater_than_80])
    print()


def export_as_xlsx(data: pd.DataFrame) -> None:
    print("---")
    print("Exporting data...")
    data.to_excel("data.xlsx")
    print("Done.")
    print()


if __name__ == "__main__":
    main()

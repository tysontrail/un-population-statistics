# main.py
#
# Group name:
# - Kernel Panic
#
# Team members:
# - Tyson Trail
# - Kevin Amado
#


# Third party libraries
import matplotlib.pyplot as plt  # Tested with matplotlib==3.5.1
import numpy as np  # Tested with numpy==1.21.5
import pandas as pd  # Tested with pandas==1.4.2
# Standard library
import textwrap
from typing import (
    Any,
    List,
    Tuple,
)


def print_dependencies_note() -> None:
    """Print the dependencies required by this program.

    Returns:
        None.
    """
    print("---")
    print("Note: this program requires the following dependencies:")
    print("    matplotlib==3.5.1")
    print("    numpy==1.21.5")
    print("    openpyxl==3.0.9")
    print("    pandas==1.4.2")
    print("    python==3.9")
    print()
    print(
        "If you encounter any error, "
        "please make sure you are using the exact versions displayed above "
        "and try again."
    )
    print()


def main() -> None:
    """Entrypoint of this program.

    Returns:
        None.
    """
    # Stage 0: Ensure user has the required dependencies.
    print_dependencies_note()

    # Stage 2: DataFrame Creation
    data: pd.DataFrame = load_and_merge_data()
    add_life_expectancy_column(data)
    add_fertility_rate_column(data)

    print_complete_dataset(data)

    # Stage 3: User Entry
    print_available_countries(data)
    country: str = get_country(data)
    country_data = data.loc[country, :]
    years: str = ", ".join(map(str, country_data.index))
    print_available_years_for_country(years)
    year: int = get_year(country_data)

    # Stage 4: Analysis and Calculations
    print_data_for_country_and_year(country, country_data, year)
    print_mean_for_all_years_for_country(country, country_data, years)
    print_stats_for_all_years_all_countries(data)
    print_fastest_growing_countries(data)
    print_countries_with_life_expectancy_over_80(data)

    # Stage 5: Export and Matplotlib
    export_as_xlsx(data)
    export_life_expectancy_as_matplotlib(data)
    export_total_fertility_rate_as_matplotlib(data)


def load_and_merge_data() -> pd.DataFrame:
    """Load data from three data sources and aggregates them into one.

    Returns:
        pd.DataFrame: A Pandas DataFrame with the merged data.
    """
    # Import your chosen data into a Pandas DataFrames.
    population_1: pd.DataFrame = pd.read_excel(
        "input-datasets/un-population-dataset-1.xlsx",
        usecols=["M49 Code", "Year", "Region/Country/Area", "Series", "Value"],
    )
    population_2: pd.DataFrame = pd.read_excel(
        "input-datasets/un-population-dataset-2.xlsx",
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
        "input-datasets/un-m49.xlsx",
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
    """Add a column with the life expectancy distance from the mean.

    Args:
        data (pd.DataFrame): Merged DataFrame as by `load_and_merge_data()`.

    Returns:
        None.
    """
    data["Life expectancy difference (years) from mean"] = (
        data["Life expectancy at birth for both sexes (years)"]
        - data["Life expectancy at birth for both sexes (years)"].mean()
    )


def add_fertility_rate_column(data: pd.DataFrame) -> None:
    """Add a column with the difference in fertility rate from the mean.

    Args:
        data (pd.DataFrame): Merged DataFrame as by `load_and_merge_data()`.

    Returns:
        None.
    """
    data["Total fertility difference (children per woman) from mean"] = (
        data["Total fertility rate (children per women)"]
        - data["Total fertility rate (children per women)"].mean()
    )


def get_country(data: pd.DataFrame) -> str:
    """Prompt the user for a valid country.

    Args:
        data (pd.DataFrame): Merged DataFrame as by `load_and_merge_data()`.

    Raises:
        ValueError: If the country is invalid.

    Returns:
        str: The country after validation.
    """
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
            print("You must enter a valid Country or Area.")

    print()
    return country


def get_year(country_data: pd.DataFrame) -> int:
    """Prompt the user for a valid year for the respective country data.

    Args:
        country_data (pd.DataFrame): _description_

    Raises:
        ValueError: If the year is not valid

    Returns:
        int: The year after validation.
    """
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
    """Print the `obj` intending by 4 spaces.

    Args:
        obj (Any): Any object that implements the `__str__` method.

    Returns:
        None.
    """
    output: str = textwrap.indent(str(obj), prefix="    ")
    print(output)


def print_available_countries(data: pd.DataFrame) -> None:
    """Print the available countries in the data.

    Args:
        data (pd.DataFrame): Merged DataFrame as by `load_and_merge_data()`.

    Returns:
        None.
    """
    print("---")
    print("Available countries:")
    print()
    print_indented(data.index.unique("Country or Area").values)
    print()


def print_complete_dataset(data: pd.DataFrame) -> None:
    """Print the complete dataset in the data

    Args:
        data (pd.DataFrame): Merged DataFrame as by `load_and_merge_data()`.

    Returns:
        None.
    """
    print("---")
    print("Complete dataset:")
    print()
    print_indented(data)
    print()


def print_available_years_for_country(years: str) -> None:
    """Print the available years.

    Args:
        years (str): A comma separated representation of the years.

    Returns:
        None.
    """
    print("---")
    print("Available Years:")
    print()
    print_indented(years)
    print()


def print_data_for_country_and_year(
    country: str,
    country_data: pd.DataFrame,
    year: int,
) -> None:
    """Print the data for a country and a year.

    Args:
        country (str): Country name.
        country_data (pd.DataFrame): DataFrame with the country data.
        year (int): The year.

    Returns:
        None.
    """
    print("---")
    print(f"Data available for {country}, year {year}:")
    print()
    print_indented(country_data.loc[year])
    print()


def print_mean_for_all_years_for_country(
    country: str,
    country_data: pd.DataFrame,
    years: str,
) -> None:
    """Print the mean for all the years of a country.

    Args:
        country (str): Country name.
        country_data (pd.DataFrame): DataFrame with the country data.
        years (str): Years separated by comma.

    Returns:
        None.
    """
    print("---")
    print(f"Aggregate mean for years: {years}, for {country}:")
    print()
    print_indented(country_data.mean(numeric_only=True))
    print()


def print_stats_for_all_years_all_countries(data: pd.DataFrame) -> None:
    """Print stats for all years and countries using the describe method.

    Args:
        data (pd.DataFrame): Merged DataFrame as by `load_and_merge_data()`.

    Returns:
        None.
    """
    # Use of .describe() method for combined dataset
    print("---")
    print("Aggregate stats for all years and all countries:")
    print()
    print_indented(data.describe().T)
    print()


def print_fastest_growing_countries(data: pd.DataFrame) -> None:
    """Print the fastest growing countries in the data.

    Args:
        data (pd.DataFrame): Merged DataFrame as by `load_and_merge_data()`.

    Returns:
        None.
    """
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
    """Print the countries with a life expectancy over 80 years.

    Args:
        data (pd.DataFrame): Merged DataFrame as by `load_and_merge_data()`.

    Returns:
        None.
    """
    # Use masking operation
    print("---")
    print("Countries with life expectancy over 80 years:")
    print()
    life_expectancy = data["Life expectancy at birth for both sexes (years)"]
    greater_than_80 = life_expectancy > 80
    print_indented(life_expectancy[greater_than_80])
    print()


def export_as_xlsx(data: pd.DataFrame) -> None:
    """Save the dataset as an xlsx file.

    Args:
        data (pd.DataFrame): Merged DataFrame as by `load_and_merge_data()`.

    Returns:
        None.
    """
    print("---")
    print("Exporting data...")
    data.to_excel("output-datasets/full-dataset.xlsx")
    data.to_csv("output-datasets/full-dataset.csv")
    print("Done.")
    print()


def export_life_expectancy_as_matplotlib(data: pd.DataFrame) -> None:
    """Create and save a comparison between life expectancy in 4 countries.

    Args:
        data (pd.DataFrame): Merged DataFrame as by `load_and_merge_data()`.

    Returns:
        None.
    """

    def _plot_country(country: str) -> None:
        """Plot the data associated to a country.

        Args:
            country (str): The country name.

        Returns:
            None.
        """
        country_data = data.loc[country, :]
        values_x = country_data.index
        values_y = country_data[
            "Life expectancy at birth for both sexes (years)"
        ]
        plt.bar(values_x, values_y, color="#66ff00")
        plt.grid(color="#cccccc", linestyle="--", axis="y", alpha=0.75)
        plt.grid(color="#cccccc", linestyle="--", axis="x", alpha=0.75)
        plt.xticks(values_x, values_x)
        plt.xlabel("Year", fontsize=10)
        plt.ylim((40, 85))
        plt.yticks(np.arange(40, 85, step=5))
        plt.ylabel("Life expectancy (years)", fontsize=10)
        plt.title(country, fontsize=10)

    plt.style.use("classic")
    figure = plt.figure()

    # List with the countries ordered by life expectancy
    countries_sorted: pd.Index = (
        data.groupby(
            "Country or Area",
        )["Life expectancy at birth for both sexes (years)"]
        .max()
        .sort_values(ascending=False)
        .index.unique("Country or Area")
    )

    # Pick only 4 countries,
    # the one with max life expectancy,
    # the one with the min life expectancy,
    # and 2 in between
    selected_countries: Tuple[str, ...] = countries_sorted[
        np.linspace(0, len(countries_sorted) - 1, num=4, dtype=np.uint64)
    ]

    figure.suptitle("Life expectancy over time", fontsize=14)
    for index in range(4):
        plt.subplot(2, 2, index + 1)
        _plot_country(selected_countries[index])

    figure.tight_layout(h_pad=1, w_pad=2)
    figure.savefig("plots/life-expectancy-over-time.png")


def export_total_fertility_rate_as_matplotlib(data: pd.DataFrame) -> None:
    """Create and save the evolution in fertility rate.

    Args:
        data (pd.DataFrame): Merged DataFrame as by `load_and_merge_data()`.

    Returns:
        None.
    """

    def _plot_year(year: int) -> None:
        """Plot the data associated to a year.

        Args:
            year (int): The year.

        Returns:
            None.
        """
        plt.hist(series, color="#66ff00")
        plt.grid(color="#cccccc", linestyle="--", axis="y", alpha=0.75)
        plt.grid(color="#cccccc", linestyle="--", axis="x", alpha=0.75)
        plt.xlabel("Number of children per women", fontsize=10)
        plt.ylim((0, 50))
        plt.yticks(np.arange(0, 50, step=10))
        plt.ylabel("Number of countries", fontsize=10)
        plt.title(f"Year {year}", fontsize=10)

    plt.style.use("classic")
    figure = plt.figure()
    figure.suptitle("Total fertility rate", fontsize=14)

    years = sorted(data.index.unique("Year"))
    for index, year in enumerate(years, start=1):
        series = data.loc[data.index.get_level_values("Year") == year][
            "Total fertility rate (children per women)"
        ]
        plt.subplot(len(years), 1, index)
        _plot_year(year)

    figure.tight_layout(h_pad=1, w_pad=2)
    figure.savefig("plots/total-fertility-rate.png")


if __name__ == "__main__":
    main()

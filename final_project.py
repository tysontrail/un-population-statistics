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


def main() -> None:
    data: pd.DataFrame = load_and_merge_data()

    print(data)


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
    )

    return data


if __name__ == "__main__":
    main()

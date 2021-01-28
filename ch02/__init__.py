from ch02.fetch_data import fetch_housing_data, load_housing_data
from ch02.look_at_data import take_quick_look_at_data, show_housing_hist
from ch02.test_set import split_train_test, split_train_test_by_id
from sklearn.model_selection import train_test_split, StratifiedShuffleSplit
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix


def run_ch02():
    fetch_housing_data()
    housing = load_housing_data()
    # take_quick_look_at_data(housing)
    # show_housing_hist(housing)
    # train_set, test_set = split_train_test(housing, 0.2)
    # print(len(train_set))
    # print(len(test_set))
    # housing_with_id = housing.reset_index()
    # train_set, test_set = split_train_test_by_id(housing_with_id, 0.2, "index")
    # housing_with_id["id"] = housing["longitude"] * 1000 + housing["latitude"]
    # train_set, test_set = split_train_test_by_id(housing_with_id, 0.2, "id")
    # train_set, test_set = train_test_split(housing, test_size=0.2, random_state=42)
    # print(len(train_set))
    # print(len(test_set))
    housing["income_cat"] = pd.cut(housing["median_income"], bins=[0., 1.5, 3.0, 4.5, 6., np.inf],
                                   labels=[1, 2, 3, 4, 5])
    # housing["income_cat"].hist()
    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    for train_index, test_index in split.split(housing, housing["income_cat"]):
        strat_train_set = housing.loc[train_index]
        strat_test_set = housing.loc[test_index]

    # strata_ratio = strat_test_set["income_cat"].value_counts() / len(strat_test_set)
    # print(strata_ratio)
    for set_ in (strat_train_set, strat_test_set):
        set_.drop("income_cat", axis=1, inplace=True)

    # housing = strat_train_set.copy()
    # housing.plot(kind="scatter", x="longitude", y="latitude")
    # housing.plot(kind="scatter", x="longitude", y="latitude", alpha=0.1)
    # housing.plot(kind="scatter", x="longitude", y="latitude", alpha=0.4,
    #              s=housing["population"]/100, label="population", figsize=(10,7),
    #              c="median_house_value", cmap=plt.get_cmap("jet"), colorbar=True)
    # plt.show()
    # corr_matrix = housing.corr()
    # print(corr_matrix["median_house_value"].sort_values(ascending=False))

    # attributes = ["median_house_value", "median_income", "total_bedrooms", "housing_median_age"]
    # scatter_matrix(housing[attributes], figsize=(12, 8))
    # plt.show()

    # housing["rooms_per_household"] = housing["total_rooms"]/housing["households"]
    # housing["bedrooms_per_room"] = housing["total_bedrooms"] / housing["total_rooms"]
    # housing["population_per_household"] = housing["population"] / housing["households"]
    #
    # corr_matrix = housing.corr()
    # corr_result = corr_matrix["median_house_value"].sort_values(ascending=False)
    # print(corr_result)

    housing = strat_train_set.drop("median_house_value", axis=1)
    housing_labels = strat_train_set["median_house_value"].copy()

    housing.dropna(subset=["total_bedrooms"])
    housing.drop("total_bedrooms", axis=1)
    median = housing["total_bedrooms"].median()
    housing["total_bedrooms"].fillna(median, inplace=True)

    from sklearn.impute import SimpleImputer
    imputer = SimpleImputer(strategy="median")
    housing_num = housing.drop("ocean_proximity", axis=1)
    imputer.fit(housing_num)

    print(imputer.statistics_)
    print(housing_num.median().values)

    X = imputer.transform(housing_num)
    housing_tr = pd.DataFrame(X, columns=housing_num.columns, index=housing_num.index)


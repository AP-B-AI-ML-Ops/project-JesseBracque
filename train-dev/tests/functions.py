""" "Functions for the testing of tasks"""

import pickle

def dump_pickle(obj, filename: str):
    """dumps object into a file"""
    with open(filename, "wb") as f_out:
        return pickle.dump(obj, f_out)

def load_pickle(filename):
    """loads pickle file from a file name"""
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)

def prepare_regression_train_or_val_data(df, dv, train):
    """Prepares the data for regression training or validation"""
    # pylint: disable=[C0103]
    df["Date"] = df["Date"].astype(str)
    categorical = ["Date"]
    numerical = ["EUR"]

    data_dict = df[categorical + numerical].to_dict(orient="records")
    Y_data = df["gold_diff"].values

    if train:
        X_data = dv.fit_transform(data_dict)
    else:
        X_data = dv.transform(data_dict)

    return X_data, Y_data

def prepare_gold_data(df, currency_col="EUR", new_col_name="gold_diff"):
    """Calculates the difference in gold value between two consecutive days"""
    df = df.copy()
    df[new_col_name] = df[currency_col].diff().fillna(0)
    return df[["Date", currency_col, new_col_name]]

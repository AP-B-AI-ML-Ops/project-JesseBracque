import os
import pickle
import click
import pandas as pd

from sklearn.feature_extraction import DictVectorizer

from prefect import task, flow


@task(log_prints=True, retries=4)
def dump_pickle(obj, filename: str):
    with open(filename, "wb") as f_out:
        return pickle.dump(obj, f_out)

 
@flow(log_prints=True)
def split_and_read_data(path):
    df = pd.read_csv(path)

    for col in df.columns:
        if col != "Date":
            df[col] = df[col].str.replace(",", "", regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce')
    df['Date'] = pd.to_datetime(df['Date'])

    total_len = len(df)
    train_end = int(0.7 * total_len)
    val_end = int(0.85 * total_len)
    
    train_df = df.iloc[:train_end].sort_values("Date")
    val_df = df.iloc[train_end:val_end].sort_values("Date")
    test_df = df.iloc[val_end:].sort_values("Date")

    return prepare_gold_data(train_df), prepare_gold_data(val_df), prepare_gold_data(test_df)


@task(log_prints=True, retries=4)
def prepare_gold_data(df, currency_col='EUR', new_col_name='gold_diff'):
    df = df.copy()
    df[new_col_name] = df[currency_col].diff().fillna(0)
    return df[['Date', currency_col, new_col_name]]


@task(log_prints=True, retries=4)
def prepare_regression_train_or_val_data(df, dv, train):
    df['Date'] = df['Date'].astype(str)
    categorical = ['Date']
    numerical = ['EUR']

    data_dict = df[categorical + numerical].to_dict(orient='records')
    Y_data = df['gold_diff'].values

    if train:
        X_data = dv.fit_transform(data_dict)
    else:
        X_data = dv.transform(data_dict)

    return X_data, Y_data


@flow(log_prints=True)
def run_data_prep(raw_data_path: str = "data-files", dest_path: str = "output", dataset: str = "Daily.csv"):
    # Load parquet files
    df_train, df_val, df_test = split_and_read_data(
        os.path.join(raw_data_path, f"{dataset}")
    )

    # Extract the target, fit DictVectorizer and preprocess data
    dv = DictVectorizer()
    X_train, y_train = prepare_regression_train_or_val_data(df_train, dv, True)
    X_val, y_val = prepare_regression_train_or_val_data(df_val, dv, False)
    X_test, y_test = prepare_regression_train_or_val_data(df_test, dv, False)

    # Create dest_path folder unless it already exists
    os.makedirs(dest_path, exist_ok=True)

    # Save DictVectorizer and datasets
    dump_pickle(dv, os.path.join(dest_path, "dv.pkl"))
    dump_pickle((X_train, y_train), os.path.join(dest_path, "train.pkl"))
    dump_pickle((X_val, y_val), os.path.join(dest_path, "val.pkl"))
    dump_pickle((X_test, y_test), os.path.join(dest_path, "test.pkl"))


if __name__ == '__main__':
    run_data_prep()
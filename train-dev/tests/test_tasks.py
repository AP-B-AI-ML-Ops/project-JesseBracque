import os
import pandas as pd
import pytest
from sklearn.feature_extraction import DictVectorizer
from tests.functions import dump_pickle, load_pickle, prepare_regression_train_or_val_data, prepare_gold_data

def test_dump_and_load_pickle():
    """Test both dump_pickle and load_pickle functions"""
    # Arrange
    test_data = {"test": "data"}
    test_filename = "test_pickle.pkl"
    
    # Act
    dump_pickle(test_data, test_filename)
    loaded_data = load_pickle(test_filename)

    # Assert
    assert os.path.exists(test_filename)
    assert loaded_data == test_data

    # Cleanup
    os.remove(test_filename)

def test_load_pickle_nonexistent_file():
    """Test load_pickle with a non-existent file"""
    with pytest.raises(FileNotFoundError):
        load_pickle("nonexistent_file.pkl")

def test_dump_pickle_invalid_path():
    """Test dump_pickle with an invalid path"""
    test_data = {"test": "data"}
    with pytest.raises(OSError):
        dump_pickle(test_data, "/invalid/path/test.pkl")

def test_prepare_regression_train_or_val_data():
    """Test prepare_regression_train_or_val_data function"""
    # Arrange
    test_df = pd.DataFrame({
        'Date': ['2023-01-01', '2023-01-02'],
        'EUR': [100.0, 101.0],
        'gold_diff': [0.0, 1.0]
    })
    test_df['Date'] = pd.to_datetime(test_df['Date'])
    dv = DictVectorizer()
    
    # Act
    X_train, y_train = prepare_regression_train_or_val_data(test_df, dv, train=True)
    assert X_train.shape[0] == 2  # Should have 2 rows
    assert y_train.shape[0] == 2
    
    # Assert
    X_val, y_val = prepare_regression_train_or_val_data(test_df, dv, train=False)
    assert X_val.shape[0] == 2
    assert y_val.shape[0] == 2

def test_prepare_regression_train_or_val_data_missing_columns():
    """Test prepare_regression_train_or_val_data with missing required columns"""
    # Arrange
    test_df = pd.DataFrame({
        'Wrong_Column': ['2023-01-01'],
        'EUR': [100.0]
    })
    dv = DictVectorizer()
    
    # Assert
    with pytest.raises(KeyError):
        prepare_regression_train_or_val_data(test_df, dv, train=True)

def test_prepare_regression_train_or_val_data_empty_df():
    """Test prepare_regression_train_or_val_data with empty DataFrame"""
    # Arrange
    test_df = pd.DataFrame(columns=['Date', 'EUR', 'gold_diff'])
    dv = DictVectorizer()
    
    # Act and assert
    with pytest.raises(ValueError):
        X_train, y_train = prepare_regression_train_or_val_data(test_df, dv, train=True)

def test_prepare_gold_data():
    """Test prepare_gold_data function"""
    # Arrange
    test_df = pd.DataFrame({
        'Date': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'EUR': [100.0, 101.0, 102.0]
    })
    test_df['Date'] = pd.to_datetime(test_df['Date'])
    
    # Act
    result_df = prepare_gold_data(test_df)
    
    # Assert
    assert len(result_df) == 3
    assert 'gold_diff' in result_df.columns
    assert result_df['gold_diff'].iloc[0] == 0  # First row should be 0
    assert result_df['gold_diff'].iloc[1] == 1.0  # Second row should be the difference (101-100)
    assert result_df['gold_diff'].iloc[2] == 1.0  # Third row should be the difference (102-101)

def test_prepare_gold_data_missing_currency():
    """Test prepare_gold_data with missing currency column"""
    # Arrange
    test_df = pd.DataFrame({
        'Date': ['2023-01-01'],
        'Wrong_Currency': [100.0]
    })
    test_df['Date'] = pd.to_datetime(test_df['Date'])
    
    # Assert
    with pytest.raises(KeyError):
        prepare_gold_data(test_df, currency_col="EUR")

def test_prepare_gold_data_invalid_date():
    """Test prepare_gold_data with invalid date format"""
    # Arrange
    test_df = pd.DataFrame({
        'Date': ['invalid_date'],
        'EUR': [100.0]
    })
    
    # Assert
    with pytest.raises(pd._libs.tslibs.parsing.DateParseError):
        test_df['Date'] = pd.to_datetime(test_df['Date'])
        prepare_gold_data(test_df)
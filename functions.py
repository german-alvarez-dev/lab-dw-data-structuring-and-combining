import pandas as pd

def normalize_column_names(df):
    df_normalized = df.copy()
    df_normalized.columns = df_normalized.columns.str.lower().str.replace(" ", "_")
    df_normalized.rename(columns={"st": "state"}, inplace=True)
    print('Column names normalized')
    return df_normalized

def clean_invalid_values(df):

    # Dictionaries mapping values
    gender_dict ={"Male": "M", "female": "F", "Female": "F", "Femal": "F"}
    education_dict = {"Bachelors": "Bachelor"}
    state_dict = {"AZ": "Arizona", "Cali": "California", "WA": "Washington"}

    # Create a dictionary to store the column-specific dictionaries
    column_dicts = {"gender": gender_dict, "education": education_dict, "state": state_dict}

    # Loop through each column in the dataset and clean the inconsistent values using the corresponding dictionary mapping
    for col in column_dicts:
        df[col] = df[col].replace(column_dicts[col])

    print('Inconsistent values replaced')

    # Clean the data in 'Customer Lifetime Value'
    df['customer_lifetime_value'] = df['customer_lifetime_value'].str.replace('%', '')
    df['customer_lifetime_value'] = pd.to_numeric(df['customer_lifetime_value'], errors='coerce')
    df['customer_lifetime_value'].head()

    # similar values grouped
    luxury = ["Sports Car", "Luxury SUV", "Luxury Car"]
    df["vehicle_class"] = df["vehicle_class"].apply(lambda x: "Luxury" if x in luxury else x)

    return df

def remove_null_values(df):
    # Identify any columns with null or missing values
    null_cols = df.columns[df.isnull().any()]

    # Print the columns with null or missing values
    print("Columns with null or missing values:")
    print(null_cols)

    # Separate categorical and numerical variables
    cat_vars = df.select_dtypes(include=["object"]).columns
    num_vars = df.select_dtypes(include=["float64", "int64"]).columns

    # Fill null values in categorical variables with the mode
    for col in null_cols:
        if col in cat_vars:
            df[col].fillna(df[col].mode()[0], inplace=True)

    # Fill null values in numerical variables with the mean
    for col in null_cols:
        if col in num_vars:
            df[col].fillna(df[col].mean(), inplace=True)

    # Verify that all null values have been handled
    null_cols = df.columns[df.isnull().any()]
    if len(null_cols) == 0:
        print("All null values have been successfully handled")
    else:
        print("Null values still exist in the following columns:")
        print(null_cols)
    
    return df
#############################################
# Lead Calculation with Rule-Based Classification
#############################################

#############################################
# Business Problem
#############################################

# A game company wants to create a new level-based persona using some features of its customers.
# Then, it also wants to determine segments according to these personas,
# and estimate how much new customers can earn on average according to these segments.

# EXAMPLE:
# Estimate how much a 25-year-old male user from Turkey who is an IOS user can earn on average.

import pandas as pd
df = pd.read_csv('/Users/hikmetburakozcan/Desktop/persona.csv')

def get_info_about_dataset(dataframe):
    print(45*"#", "THE FIRST 5 OBSERVATIONS IN THE DATASET", 45*"#", dataframe.head(), sep='\n', end = '\n\n')
    print(45*"#", "THE LAST 5 OBSERVATIONS IN THE DATASET", 45*"#", dataframe.tail(), sep='\n', end = '\n\n')
    print(45*"#", f"THE TOTAL NUMBER OF OBSERVATIONS IN THE DATASET: {dataframe.shape[0]}", 45*"#", sep='\n', end = '\n\n')
    print(45*"#", f"THE NUMBER OF VARIABLES IN THE DATASET: {dataframe.shape[1]}", 45*"#", sep='\n', end = '\n\n')
    print(45*"#", "THE NUMBER OF MISSING VALUES FOR EACH VARIABLES", 45*"#", dataframe.isnull().sum(), sep='\n', end = '\n\n')
    print(45*"#", "THE TYPES OF VARIABLES IN THE DATASET", 45*"#", dataframe.dtypes, sep='\n', end = '\n\n')
    print(45*"#", "DESCRIPTIVE STATISTICS OF NUMERICAL VARIABLES", 45*"#", dataframe.describe(percentiles=[0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99]).T, sep='\n', end = '\n\n')
    print(45*"#", "DESCRIPTIVE STATISTICS OF CATEGORICAL VARIABLES", 45*"#", dataframe.describe(include=object).T, sep='\n', end = '\n\n')

get_info_about_dataset(df)

def aggregate_dataframe(dataframe, columns, target, measures_list = ["mean"]):
    for col in columns:
        print(20*"#", dataframe.groupby(by = col).agg({target: measures_list}), sep = '\n', end = '\n\n')
    
    print(35*"#", dataframe.groupby(by = columns).agg({target: measures_list}), sep = '\n')
    return dataframe.groupby(by = columns).agg({target: measures_list})


df_agg = aggregate_dataframe(df, ["COUNTRY", 'SOURCE', "SEX", "AGE"], "PRICE")

def define_persona(dataframe):
    dataframe.reset_index(inplace = True)
    dataframe["AGE_CAT"] = pd.cut(dataframe["AGE"], bins = [0, 18, 23, 30, 40, dataframe["AGE"].max()], labels = ['0_18', '19_23', '24_30', '31_40', '41_' + str(dataframe["AGE"].max())])
    dataframe.columns = dataframe.columns.get_level_values(0)
    dataframe["CUSTOMER_LEVEL_BASED"] = [observations[0].upper() + "_" + observations[1].upper() + "_" + observations[2].upper() + "_" + observations[5].upper() for observations in dataframe.values]
    return dataframe[["CUSTOMER_LEVEL_BASED", "PRICE"]].groupby("CUSTOMER_LEVEL_BASED").agg({"PRICE": "mean"}).reset_index(inplace = True)

df_final = define_persona(df_agg)
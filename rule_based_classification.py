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

def get_info_about_dataset(dataframe):
    print(45*"#", "THE FIRST 5 OBSERVATIONS IN THE DATASET", 45*"#", dataframe.head(), sep='\n', end = '\n\n')
    print(45*"#", "THE LAST 5 OBSERVATIONS IN THE DATASET", 45*"#", dataframe.tail(), sep='\n', end = '\n\n')
    print(45*"#", f"THE TOTAL NUMBER OF OBSERVATIONS: {dataframe.shape[0]}", 45*"#", sep='\n', end = '\n\n')
    print(45*"#", f"THE NUMBER OF VARIABLES: {dataframe.shape[1]}", 45*"#", sep='\n', end = '\n\n')
    print(45*"#", "THE NUMBER OF MISSING VALUES FOR EACH VARIABLES", 45*"#", dataframe.isnull().sum(), sep='\n', end = '\n\n')
    print(45*"#", "THE TYPES OF VARIABLES", 45*"#", dataframe.dtypes, sep='\n', end = '\n\n')
    print(45*"#", "DESCRIPTIVE STATISTICS OF NUMERICAL VARIABLES", 45*"#", dataframe.describe(percentiles=[0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99]).T, sep='\n', end = '\n\n')
    print(45*"#", "DESCRIPTIVE STATISTICS OF CATEGORICAL VARIABLES", 45*"#", dataframe.describe(include=object).T, sep='\n', end = '\n\n')

def aggregate_dataframe(dataframe, columns, target, measure = "mean"):
    for col in columns:
        print(25*"#", "Average {} by {}".format(target, col), 25*"#", dataframe.groupby(by = col).agg({target: measure}), sep = '\n', end = '\n\n')
    
    print(40*"#", "Average {} by {}".format(target, columns), 40*"#", dataframe.groupby(by = columns).agg({target: measure}), sep = '\n')
    return dataframe.groupby(by = columns).agg({target: measure})

def persona_dataframe(dataframe, target, measure = "mean"):
    dataframe.reset_index(inplace = True)
    dataframe["AGE_CAT"] = pd.cut(dataframe["AGE"], bins = [0, 18, 23, 30, 40, dataframe["AGE"].max()], labels = ['0_18', '19_23', '24_30', '31_40', '41_' + str(dataframe["AGE"].max())])
    dataframe["CUSTOMER_LEVEL_BASED"] = [observations[0].upper() + "_" + observations[1].upper() + "_" + observations[2].upper() + "_" + observations[5].upper() for observations in dataframe.values]
    persona_df = dataframe[["CUSTOMER_LEVEL_BASED", target]].groupby("CUSTOMER_LEVEL_BASED").agg({target: measure})
    persona_df.reset_index(inplace = True)
    persona_df["SEGMENT"] = pd.qcut(persona_df["PRICE"], 4, labels=["D", "C", "B", "A"])
    print(35*"#", "PERSONA DATAFRAME", 35*"#", persona_df, sep = '\n')
    return persona_df

def new_user():
    country = input("Choose your country abbreviations from the list {}: ".format(df["COUNTRY"].unique()))
    source = input("Choose your source from the list {}: ".format(df["SOURCE"].unique()))
    gender = input("Choose your gender from the list {}: ".format(df["SEX"].unique()))
    age_range = input("Choose your age range from the list {}: ".format(agg_df["AGE_CAT"].unique()))

    return country.upper() + "_" + source.upper() + "_" + gender.upper() + "_" + age_range


if __name__ == "__main__":
    df = pd.read_csv('/Users/hikmetburakozcan/Desktop/DSMLBC10-Databusters/Week_1/persona.csv')
    get_info_about_dataset(df)
    agg_df = aggregate_dataframe(df, ["COUNTRY", 'SOURCE', "SEX", "AGE"], "PRICE")
    persona_df = persona_dataframe(agg_df, "PRICE")
    user = new_user()
    persona_df[persona_df["CUSTOMER_LEVEL_BASED"] == user]




from functools import reduce
import re 
import unicodedata
import pandas as pd
from collections.abc import Iterable


def pipe(*functions : callable)->callable: 
    return lambda x: reduce (lambda previous, next_: next_(previous), functions,x)


def lowercase(dataframe: pd.DataFrame, columns: Iterable[str])->pd.DataFrame: 
    for column in columns: 
        dataframe[column] = dataframe[column].str.lower()
    return dataframe

def remove_accent(dataframe:pd.DataFrame, columns : Iterable[str])->pd.DataFrame: 
    for column in columns: 
        dataframe[column] = dataframe[column].apply(
                lambda x : unicodedata.normalize("NFKD", x).encode("ASCII", "ignore").decode("ASCII")

        )
    return dataframe


def replace_special_chars(dataframe: pd.DataFrame, columns : Iterable[str])->pd.DataFrame: 
    for column in columns: 
        dataframe[column] = dataframe[column].apply(
                lambda x: re.sub(r'[^\w\s-]','_', x)
        )
    return dataframe

def replace_spaces(dataframe: pd.DataFrame, columns : Iterable[str])->pd.DataFrame: 
    for column in columns: 
        dataframe[column] = dataframe[column].apply(
                    lambda x: re.sub(r'[-\s]+', '_',x)
        )
    return dataframe


def round_numbers(dataframe: pd.DataFrame, columns: Iterable[str], decimals:int)->pd.DataFrame: 
    for column in columns:
        dataframe[column] = dataframe[column].round(decimals)
    return dataframe

def normalize_numbers(dataframe:pd.DataFrame, columns: Iterable[str])->pd.DataFrame: 
    for column in columns: 
        dataframe[column] = (
                dataframe[column] -dataframe[column].min()) / (dataframe[column].max()-dataframe[column].min()
                                                              )
        
    return dataframe

def categorize_age(dataframe: pd.DataFrame, column: str)->pd.DataFrame: 
    bins = [0,18,30,50,100]
    labels = ["Enfant", "Jeune adulte", "Adulte", "Senior"]
    dataframe[f'{column}_category'] = pd.cut(dataframe[column], bins = bins, labels = labels,
                                            right=False)
    return dataframe

def main()->pd.DataFrame: 
    data_frame = pd.DataFrame({

        "name": ["Reema", "S'hyam", "jai", "Nimish 'a", "Roh(It", "Riya 'e"],
        "gender" :["Femalé", "Male", "Mal&e", "Female", "Male", "Female"],
        "email": [
                "reema@gmail.com", "shyam@yahoo.com", 
                "jai@hotmail.com", "nimisha@gmail.com",
                "rohit@outlook.com", "riyae@gmail.com"
        ],
        "age": [31, 32,19,23,28,33], 
        "salary" : [50000.75, 60000.50, 30000.25, 45000, 55000.00, 62000.90]
    })

     
    pipeline =  (data_frame
                 .pipe(lowercase, columns = ["name", "gender", "email"])
                 .pipe(remove_accent, columns = ["name", "gender"])
                 .pipe(replace_special_chars, columns =["name", "gender"]  )
                 .pipe(replace_spaces, columns = ["name", "gender"])
                 .pipe(round_numbers, columns =["salary"],decimals = 2)
                 .pipe(normalize_numbers, columns = ["salary"])
                 .pipe(categorize_age, column = "age"))
                
    return data_frame,pipeline


if __name__ == "__main__": 
    data_frame , data_cleaned = main()
    print(data_frame)
    print("\n")
    print(data_cleaned)
    data_frame.to_csv("data_not_cleaned.csv")
    data_cleaned.to_csv("data_cleaned.csv")
#!/usr/bin/env python3
import pandas as pd, numpy as np, openpyxl
from string import ascii_uppercase
from itertools import product


def long2square(df: pd.DataFrame, col: str, index: str):
    currDf = df.set_index(index)
    wellLetter = [i for i in ascii_uppercase[:16]]
    wellNumber = [i for i in range(1, 25)]

    plateLayout = pd.DataFrame(0, index=wellLetter, columns=wellNumber, dtype=str)

    for idx, value in currDf[col].items():
        currLetter = idx[0]
        currNumber = int(idx[1:])
        plateLayout.at[currLetter, currNumber] = value

    plateLayout.index.name = "well_letter"
    plateLayout.columns.name = "well_number"
    plateLayout.rename(columns=lambda x: str(x).zfill(2), inplace=True)
    return plateLayout


def square2long(df: pd.DataFrame, col: str, index: str):
    df = df.copy()
    well = ["".join([x, y]) for x, y in product(df.index, df.columns)]
    df.rename(columns=lambda x: str(x).zfill(2), inplace=True)
    listLayout = pd.DataFrame(0, index=well, columns=[col], dtype=str)
    listLayout.index.name = index

    for idx, row in df.iterrows():
        for col in df.columns:
            listLayout.loc[f"{idx}{col}"] = row[col]

    return listLayout


def platemap2square(df: pd.DataFrame, index: str, outPath: str):
    with pd.ExcelWriter(outPath, engine="openpyxl") as writer:
        for col in df.columns:
            if index != col:
                convDf = long2square(df=df, index=index, col=col)
                convDf.to_excel(writer, sheet_name=col)
    return


def main():
    testFile = "/Users/dterciano/Desktop/LokeyLabFiles/TargetMol/platemaps/2023-11-16TargetMol_10uMcompound_PMA_Echotransfer.xlsx"
    platemap = pd.read_excel(testFile, sheet_name="noPMAplate")
    platemap2square(df=platemap, index="384_Well", outPath="~/Desktop/test.xlsx")
    return


if __name__ == "__main__":
    main()

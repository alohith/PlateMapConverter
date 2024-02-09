#!/usr/bin/env python3
import pandas as pd, numpy as np
from string import ascii_uppercase
from itertools import product
import os, sys


def long2square(
    df: pd.DataFrame, col: str, index: str, width: int = 24, height: int = 16
) -> pd.DataFrame:
    currDf = df.set_index(index)
    wellLetter = [i for i in ascii_uppercase[:height]]
    wellNumber = [i for i in range(1, width + 1)]

    plateLayout = pd.DataFrame(0, index=wellLetter, columns=wellNumber, dtype=str)

    for idx, value in currDf[col].items():
        currLetter = idx[0]
        currNumber = int(idx[1:])
        plateLayout.at[currLetter, currNumber] = value

    plateLayout.index.name = "well_letter"
    plateLayout.columns.name = "well_number"
    plateLayout.rename(columns=lambda x: str(x).zfill(2), inplace=True)
    return plateLayout


def square2long(df: pd.DataFrame, col: str, index: str) -> pd.DataFrame:
    df.rename(columns=lambda x: str(x).zfill(2), inplace=True)
    well = ["".join([x, y]) for x, y in product(df.index, df.columns)]
    listLayout = pd.DataFrame(0, index=well, columns=[col], dtype=str)
    listLayout.index.name = index

    for idx, row in df.iterrows():
        for col in df.columns:
            listLayout.loc[f"{idx}{col}"] = row[col]

    return listLayout


def platemap2square(
    df: pd.DataFrame, index: str, outPath: str, width: int = 24, height: int = 16
):
    with pd.ExcelWriter(outPath, engine="openpyxl") as writer:
        for col in df.columns:
            if index != col:
                convDf = long2square(
                    df=df, index=index, col=col, width=width, height=height
                )
                convDf.to_excel(writer, sheet_name=col)
    return


def sqaure2platemap(inFile: str, index: str) -> pd.DataFrame:
    resDfs = []
    with pd.ExcelFile(inFile) as xlsx:
        sheetNames = xlsx.sheet_names
        for sheet in sheetNames:
            df = pd.read_excel(inFile, sheet_name=sheet, index_col=0)

            if not isSquare(df=df):
                print(f"ERROR: {inFile} is not in square form!", file=sys.stderr)
                sys.exit(1)

            formattedCols = square2long(df=df, index=index, col=sheet)
            resDfs.append(formattedCols)

    return pd.concat(resDfs, axis=1)


def isSquare(df: pd.DataFrame) -> bool:
    if len(df.columns) == 24 and len(df.index) == 16:  # 16 * 24 = 384
        try:
            [
                int(i)
                for i in df.columns  # in square form, the column labels are numerical
            ]
            return True
        except ValueError:
            return False

    return False

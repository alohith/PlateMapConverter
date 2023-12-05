#!/usr/bin/env python3
import pandas as pd, numpy as np, openpyxl
from string import ascii_uppercase
from itertools import product
import sys


def long2square(df: pd.DataFrame, col: str, index: str) -> pd.DataFrame:
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


def square2long(df: pd.DataFrame, col: str, index: str) -> pd.DataFrame:
    df.rename(columns=lambda x: str(x).zfill(2), inplace=True)
    well = ["".join([x, y]) for x, y in product(df.index, df.columns)]
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


class CommandLine:
    def __init__(self, inOpts=None) -> None:
        import argparse

        self.parser = argparse.ArgumentParser(
            description="A simple 384 platemap converter",
            epilog="can convert from array form to square form and vice versa",
            prog="simple384PlatermapConverter.py",
            add_help=True,
            prefix_chars="-",
            usage="python3 %(prog)s -i <input> -o <outpath> [long2square | square2long]",
        )
        self.subparser = self.parser.add_subparsers(
            title="program options", dest="subcommand"
        )

        self.parser.add_argument(
            "-i",
            "--input",
            action="store",
            required=True,
            nargs="?",
            help="input file path",
            type=str,
        )
        self.parser.add_argument(
            "-o",
            "--output",
            action="store",
            required=True,
            nargs="?",
            help="output file path",
            type=str,
        )
        self.parser.add_argument(
            "-c",
            "--columnIndex",
            nargs="?",
            required=True,
            help="The 'index' column of your platemap (i.e. 384_Well)",
            type=str,
        )

        self.long2square = self.subparser.add_parser(
            "long2square",
            help="converts array form platemap to square form plate format",
            add_help=True,
        )
        self.square2long = self.subparser.add_parser(
            "square2long",
            help="converts square form platemap (input must be xlsx file) to array form",
            add_help=True,
        )

        if inOpts is None:
            self.args = self.parser.parse_args()
        else:
            self.args = self.parser.parse_args(inOpts)


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


def main(inOpts=None):
    # testFile = "/Users/dterciano/Desktop/LokeyLabFiles/TargetMol/platemaps/2023-11-16TargetMol_10uMcompound_PMA_Echotransfer.xlsx"
    # platemap = pd.read_excel(testFile, sheet_name="noPMAplate")
    # platemap.to_excel("./Examples/tm_refMap.xlsx", index=False)
    # platemap2square(df=platemap, index="384_Well", outPath="~/Desktop/test.xlsx")

    # pm = sqaure2platemap(inFile="~/Desktop/test.xlsx", index="385_Well")
    # pm.to_csv("~/Desktop/yay.csv")
    cl = CommandLine(inOpts=inOpts)

    inputPath = cl.args.input
    outputPath = cl.args.output
    index = cl.args.columnIndex

    if cl.args.subcommand == "long2square":
        df = pd.read_csv(inputPath)

        if isSquare(df=df):
            print(f"ERROR: {inputPath} is in square form already!", file=sys.stderr)
            sys.exit(1)

        try:
            platemap2square(df=df, index=index, outPath=outputPath)
        except IndexError:
            print(
                f"IndexError: index of {index} not found",
                file=sys.stderr,
            )
            sys.exit(1)
    elif cl.args.subcommand == "square2long":
        df = sqaure2platemap(inFile=inputPath, index=index)
        df.to_csv(outputPath)
    else:
        cl.parser.print_usage(file=sys.stderr)
        sys.exit(1)

    return 0


if __name__ == "__main__":
    main()

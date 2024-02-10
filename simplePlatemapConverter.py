#!/usr/bin/env python3
import pandas as pd, numpy as np
import os, sys

import customtkinter as ctk
from converterModules import *
from gui_utils import *
import tkinter as tk
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


def errorMessage(message: str):
    messagebox.showerror(title="Error", message=message)


class App(ctk.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title("Platemap converter")
        self.geometry("500x600")
        self.titleLab = ctk.CTkLabel(
            master=self, text="Simple Platemap Converter", font=("Arial", 30, "bold")
        )
        self.titleLab.pack(side="top", fill="x", expand=True, padx=20, pady=(15, 5))

        self.resizable(width=False, height=False)

        self.browse = BrowseFile(master=self)
        self.browse.pack(side="top", pady=15, padx=(5, 5))

        self.options = Options(master=self)
        self.options.pack(side="top", pady=10, padx=10, fill="both", expand=True)

        self.btn_submit = ctk.CTkButton(
            master=self,
            width=200,
            height=35,
            text="Submit",
            font=("Arial", 12, "bold"),
            command=lambda: self.submit(),
        )
        self.btn_submit.pack(side="bottom", padx=10, pady=10, fill="x", expand=False)

    def submit(self):
        inFile = self.browse.getFilePath
        if inFile == "":
            errorMessage(message="No file Input")
        else:
            inFileExt = os.path.splitext(inFile)[-1]
            options = self.options.getOptions
            options["index"] = self.options.indexInput.get()
            if not options["384"]:
                width, height = 12, 8
            else:
                width, height = 24, 16

            if options["index"] == "":
                errorMessage(message="Please specify the index column")
            else:
                if options["long2sq"]:
                    outFile = self.downloadProcess(type=".xlsx")
                else:
                    outFile = self.downloadProcess()

                if not options["long2sq"]:
                    df = sqaure2platemap(inFile=inFile, index=options["index"])
                    df.to_csv(outFile)
                elif options["long2sq"]:
                    df = (
                        pd.read_csv(inFile)
                        if inFileExt == ".csv"
                        else pd.read_excel(inFile)
                    )

                    if isSquare(df=df):
                        errorMessage(message="The file input is already a square")
                        pass
                    else:
                        platemap2square(
                            df=df,
                            index=options["index"],
                            outPath=outFile,
                            width=width,
                            height=height,
                        )

    def downloadProcess(self, type=".csv"):
        filePath = ctk.filedialog.asksaveasfilename(defaultextension=type)
        return filePath


if __name__ == "__main__":
    app = App()
    app.mainloop()

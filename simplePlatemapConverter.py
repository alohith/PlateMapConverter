#!/usr/bin/env python3
import pandas as pd, numpy as np
import os, sys

import customtkinter as ctk
from converterModules import *
from gui_utils import *

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class App(ctk.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title("Platemap converter")
        self.geometry("400x600")
        self.titleLab = ctk.CTkLabel(
            master=self, text="Simple Platemap Converter", font=("Arial", 25, "bold")
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
        print(inFile)


if __name__ == "__main__":
    app = App()
    app.mainloop()

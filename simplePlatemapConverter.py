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
        self.geometry("1280x720")

        self.resizable(width=False, height=False)

        self.browse = BrowseFile(master=self)
        self.browse.pack(side="top", pady=15, padx=(5, 5))

        self.inFile = self.browse.filePath.get()


def main():
    app = App()
    app.mainloop()

    return


if __name__ == "__main__":
    main()

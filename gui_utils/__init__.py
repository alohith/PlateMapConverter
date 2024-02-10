#!/usr/bin/env python3

import customtkinter as ctk


class BrowseFile(ctk.CTkFrame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.titleText = ctk.CTkLabel(
            master=self, text="File Input", font=("Arial", 20, "bold")
        )
        self.titleText.pack(side="top", padx=5, pady=(5, 10), fill="x", expand=True)

        self.filePath = ctk.StringVar()

        self.entry = ctk.CTkEntry(self, textvariable=self.filePath, width=200)
        self.entry.pack(side="left", fill="x", expand=True, padx=2, pady=10)

        self.browse_button = ctk.CTkButton(
            self, text="Browse", command=self.browse_file, font=("Arial", 20, "bold")
        )
        self.browse_button.pack(side="right", padx=(5, 10), pady=10)

    def browse_file(self):
        # Open the file dialog to choose a file
        file_path = ctk.filedialog.askopenfilename()

        # Update the entry with the selected file path
        if file_path:  # Ensure a file path was selected
            self.filePath.set(file_path)

    @property
    def getFilePath(self):
        return self.filePath.get()


class Options(ctk.CTkFrame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.optionsKwargs = {
            "384": True,
            "long2sq": True,
        }
        self.text = ctk.CTkLabel(
            master=self, text="Options", font=("Arial", 25, "bold")
        )
        self.text.pack(side="top", padx=15, pady=(10, 5))

        ## Well type selection ##
        self.wellTypeFrame = ctk.CTkFrame(master=self)
        self.wellTypeFrame.pack(
            side="left", padx=10, pady=15, expand=True, fill="x", anchor="center"
        )

        self.wellTypeText = ctk.CTkLabel(
            master=self.wellTypeFrame, text="Well type", font=("Arial", 16, "bold")
        )
        self.wellTypeText.pack(side="top", anchor="center", pady=10, padx=10)

        # buttons below
        self.selectedWellType = ctk.StringVar(value="None")
        self.btn_384 = ctk.CTkRadioButton(
            master=self.wellTypeFrame,
            width=100,
            height=20,
            value=384,
            text="384 well type",
            command=lambda: self.changeOption(opt_384=True),
            variable=self.selectedWellType,
        )
        self.btn_384.pack(side="top", anchor="center", padx=5, pady=5)

        self.btn_96 = ctk.CTkRadioButton(
            master=self.wellTypeFrame,
            width=100,
            height=20,
            value=96,
            text="96 well type",
            command=lambda: self.changeOption(opt_384=False),
            variable=self.selectedWellType,
        )
        self.btn_96.pack(side="top", anchor="center", padx=5, pady=5)

        ## Input type selection ##
        self.inputTypeFrame = ctk.CTkFrame(master=self)
        self.inputTypeFrame.pack(
            side="right", padx=10, pady=15, expand=True, fill="x", anchor="center"
        )

        self.inputTypeText = ctk.CTkLabel(
            master=self.inputTypeFrame, text="Input Type", font=("Arial", 16, "bold")
        )
        self.inputTypeText.pack(side="top", anchor="center", pady=10, padx=10)

        # buttons below
        self.btn_inputTypeVar = ctk.StringVar(value="None")
        self.btn_long2square = ctk.CTkRadioButton(
            master=self.inputTypeFrame,
            text="List -> Square",
            width=100,
            height=20,
            value="l2s",
            command=lambda: self.changeOption(opt_long2sq=True),
            variable=self.btn_inputTypeVar,
        )
        self.btn_long2square.pack(side="top", anchor="center", padx=5, pady=5)

        self.btn_square2long = ctk.CTkRadioButton(
            master=self.inputTypeFrame,
            width=100,
            height=20,
            text="Square -> List",
            value="s2l",
            variable=self.btn_inputTypeVar,
            command=lambda: self.changeOption(opt_long2sq=False),
        )
        self.btn_square2long.pack(side="top", anchor="center", padx=5, pady=5)

    def changeOption(self, opt_384: bool = True, opt_long2sq: bool = True) -> None:
        if not opt_384:
            self.optionsKwargs["384"] = False

        if not opt_long2sq:
            self.optionsKwargs["long2sq"] = False
        print(self.optionsKwargs)

    @property
    def getOptions(self):
        return self.optionsKwargs

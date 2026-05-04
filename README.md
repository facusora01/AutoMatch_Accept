<div align="center">

<img src="Images/icon/icon.ico" width="256" alt="AutoMatch Accept Logo">

```text
    _         _        __  __       _       _     
   / \  _   _| |_ ___ |  \/  | __ _| |_ ___| |__  
  / _ \| | | | __/ _ \| |\/| |/ _` | __/ __| '_ \ 
 / ___ \ |_| | || (_) | |  | | (_| | || (__| | | |
/_/   \_\__,_|\__\___/|_|  |_|\__,_|\__\___|_| |_|
                                                  
     _                     _   
    / \   ___ ___ ___ _ __| |_ 
   / _ \ / __/ __/ _ \ '_ \ __|
  / ___ \ (_| (_|  __/ |_) | |_
 /_/   \_\___\___\___| .__/ \__|
                     |_|       
```

**AutoMatch Accept**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)

</div>

---

## Overview

**AutoMatch Accept** is an open-source program designed to automatically detect and accept match invitations for various games, such as **Counter-Strike 2 (CS2)** and **League of Legends (LoL)**.

It uses computer vision and image recognition to eliminate false positives. It includes an interactive console menu so you can select exactly which game you are queueing for before starting the search.

---

## Features

* **Multi-Game Support:** Configured for CS2 and LoL out of the box, but easily expandable to other titles.
* **Interactive Menu:** Choose the specific game before monitoring to avoid conflicts between similar UI colors/images.
* **Image-Based Recognition:** Relies on OpenCV template matching rather than basic pixel colors. It works on any client language, as long as the "Accept" button screenshot matches your game.
* **Safety Hotkeys:** Press `ESC` or the ``` ` 
``` (backtick) key at any time to safely stop the background script.

---

## Prerequisites

You must have Python installed on your system. Before running the code, ensure you install the necessary dependencies included in the repository.

---

## Installation & Usage

**1. Clone the repository**
Download or clone the project files to your local machine.

**2. Setup the Images directory**
Ensure your folder structure is correct:
* `Images/cs2.png`
* `Images/lol.png`
* `Images/icon/icon.ico` (Application icon)

**3. Install dependencies**
Open a terminal in the project folder and run:
```bash
pip install -r requirements.txt
```

**4. Run the application**
Start the script from your terminal:
```bash
python AcceptGame.py
```

**5. Select your game**
The console will display a menu. Type `1` for CS2, `2` for LoL, or `0` to exit. Press Enter and let the script run in the background.

---

## Compilation (Standalone Executable)

This project includes `pyinstaller` in its dependencies, allowing you to compile the script into a standalone `.exe` file.

To compile and include the icon in the executable, use the following command:
```bash
pyinstaller --onefile --icon=Images/icon/icon.ico AcceptGame.py
```

> **Note:** After compilation, make sure to copy your `Images` folder into the same directory where your newly generated executable is located so the program can find the button images.

Or you can just use the [latest release](https://github.com/facusora01/LoLAcceptButton/releases/latest).
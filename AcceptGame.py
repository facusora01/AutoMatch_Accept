import pyautogui
import os
def GetImagePaths():
    ImagePaths = []
    currentDirectory = os.path.dirname(os.path.abspath(__file__))
    imageDirectory = os.path.join(currentDirectory, "Images")
    for Image in os.listdir(imageDirectory):
        if Image.endswith(".png"):
            ImagePaths.append(os.path.join(imageDirectory, Image))
    return ImagePaths

def Capture():
    return pyautogui.screenshot()

def SearchImage(Screenshot, Image, confidence=0.8):
    try:
        Location = pyautogui.locateCenterOnScreen(Image, confidence=confidence, region=(0 , 0, Screenshot.width, Screenshot.height))
    except Exception as e:
        print(f"Error searching {os.path.basename(Image)}: {e}")
        Location = None
    return Location

def AcceptGame():
    ImagePaths = GetImagePaths()
    print(f"Loaded {len(ImagePaths)} images to search")
    print("Searching for Accept button...")
    while True:
        Screenshot = Capture()
        for Image in ImagePaths:
            AcceptButton = SearchImage(Screenshot, Image)
            if AcceptButton:
                print(f"Found Accept button at {AcceptButton}")
                pyautogui.click(AcceptButton)
                return

def main():
    AcceptGame()
    print("Game Accepted")
    return 0

main()
import pyautogui
import os
import cv2
import numpy as np
import time
import keyboard
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

def SearchImage(Screenshot, Image, confidence=0.7):
    try:
        # Convertir screenshot a numpy array
        screenshot_np = np.array(Screenshot)
        screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)
        
        # Leer imagen de referencia
        template = cv2.imread(Image, cv2.IMREAD_GRAYSCALE)
        
        # Buscar en múltiples escalas (0.5x a 1.5x)
        for scale in np.linspace(0.5, 1.5, 20):
            if scale == 1.0:
                scaled_template = template
            else:
                scaled_template = cv2.resize(template, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
            
            if scaled_template.shape[0] > screenshot_gray.shape[0] or scaled_template.shape[1] > screenshot_gray.shape[1]:
                continue
            
            result = cv2.matchTemplate(screenshot_gray, scaled_template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val >= confidence:
                h, w = scaled_template.shape
                center_x = max_loc[0] + w // 2
                center_y = max_loc[1] + h // 2
                return pyautogui.Point(x=center_x, y=center_y)
    except Exception as e:
        Location = None
    return None

def AcceptGame():
    global running
    running = True
    
    def stop_program(e):
        global running
        running = False
        print("\nStopping...")
    
    # Register global hotkey for backtick (`)
    keyboard.on_press_key("`", stop_program)
    
    ImagePaths = GetImagePaths()
    print(f"Loaded {len(ImagePaths)} images to search")
    print("Searching for Accept button...")
    print("Press ` (backtick) to stop\n")
    
    while running:
        Screenshot = Capture()
        for Image in ImagePaths:
            if not running:
                break
            AcceptButton = SearchImage(Screenshot, Image)
            if AcceptButton:
                print(f"Found Accept button at {AcceptButton}")
                pyautogui.click(AcceptButton)
                print("Game Accepted, waiting 3 seconds before searching again...")
                time.sleep(3)  # Cooldown para evitar clics múltiples
                break
    
    keyboard.unhook_all()

def main():
    AcceptGame()
    return 0

main()
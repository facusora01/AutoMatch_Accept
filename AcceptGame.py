import pyautogui
import os
import cv2
import numpy as np
import time
import keyboard  # Reemplazamos ctypes por keyboard

timeSleep = 10
running = False

def stop_program():
    global running
    running = False
    print("\nStopping...")

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

def SearchImage(Screenshot, Image, confidence=0.85):
    # (El código de tu función SearchImage queda exactamente igual, no necesita cambios)
    try:
        screenshot_np = np.array(Screenshot)
        screenshot_rgb = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        screen_h, screen_w = screenshot_rgb.shape[:2]
        
        template_gray = cv2.imread(Image, cv2.IMREAD_GRAYSCALE)
        template_color = cv2.imread(Image, cv2.IMREAD_COLOR)
        if template_gray is None or template_color is None:
            return None
        
        flat_threshold = 15
        is_flat_color = np.std(template_gray) < flat_threshold
        
        if is_flat_color:
            avg_color = np.mean(template_color, axis=(0, 1))
            tolerance = 15
            mask = cv2.inRange(screenshot_rgb, avg_color - tolerance, avg_color + tolerance)
            num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=8)
            
            min_area = (template_color.shape[0] * template_color.shape[1]) * 0.5
            max_area = (template_color.shape[0] * template_color.shape[1]) * 2.0
            
            for i in range(1, num_labels):
                area = stats[i, cv2.CC_STAT_AREA]
                if area < 25:
                    continue
                if min_area <= area <= max_area:
                    width = stats[i, cv2.CC_STAT_WIDTH]
                    height = stats[i, cv2.CC_STAT_HEIGHT]
                    if width > 0 and height > 0:
                        ratio = width / height
                        if ratio < 0.7 or ratio > 1.4:
                            continue
                    cx, cy = int(centroids[i][0]), int(centroids[i][1])
                    if cx >= 20 and cy >= 20 and cx <= screen_w - 20 and cy <= screen_h - 20:
                        return pyautogui.Point(x=cx, y=cy)
            return None
        
        for scale in np.linspace(0.5, 1.5, 20):
            scaled_template = cv2.resize(template_gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
            if scaled_template.shape[0] < 20 or scaled_template.shape[1] < 20:
                continue
            if scaled_template.shape[0] > screen_h or scaled_template.shape[1] > screen_w:
                continue
            
            result = cv2.matchTemplate(cv2.cvtColor(screenshot_rgb, cv2.COLOR_BGR2GRAY), scaled_template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val >= confidence:
                h, w = scaled_template.shape
                center_x = max_loc[0] + w // 2
                center_y = max_loc[1] + h // 2
                
                if center_x < 20 or center_y < 20 or center_x > screen_w - 20 or center_y > screen_h - 20:
                    continue
                return pyautogui.Point(x=center_x, y=center_y)
    except Exception:
        pass
    return None

def AcceptGame():
    global running
    running = True

    # Registramos los atajos globales para detener el programa asíncronamente
    keyboard.add_hotkey('esc', stop_program)
    keyboard.add_hotkey('`', stop_program)

    ImagePaths = GetImagePaths()
    print("Searching for Accept button...")
    print("Press ` (backtick) or ESC to stop\n")
    
    while running:
        Screenshot = Capture()
        
        for Image in ImagePaths:
            if not running: # Se rompe el ciclo si presionaste ESC durante la ejecución
                break
                
            AcceptButton = SearchImage(Screenshot, Image)
            
            if AcceptButton:
                print(f"Found Accept button at {AcceptButton}")
                pyautogui.click(AcceptButton)
                print(f"Game Accepted, waiting {timeSleep} seconds before searching again...")
                
                # En lugar de un sleep absoluto de 10 segundos, hacemos chequeos de 1 segundo
                # Esto permite que el programa se cierre instantáneamente si presionas ESC mientras espera
                for _ in range(timeSleep):
                    if not running:
                        break
                    time.sleep(1)
                break

def main():
    AcceptGame()
    return 0

if __name__ == '__main__':
    main()
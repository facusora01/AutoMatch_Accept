import pyautogui
import os
import cv2
import numpy as np
import time
import keyboard
import json
import sys
from pathlib import Path

APP_NAME = "AutoMatch_Accept"

def get_config_path():
    local_app_data = os.getenv('LOCALAPPDATA')
    config_dir = Path(local_app_data) / APP_NAME
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "config.json"

CONFIG_FILE = get_config_path()

def load_config():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                return data.get("timeSleep", 3)
        except:
            return 3
    return 3

def save_config(time_value):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump({"timeSleep": time_value}, f)
    except Exception:
        pass

timeSleep = load_config()
running = False

def stop_program():
    print("\nDeteniendo...")
    os._exit(0)

def get_image_path(filename):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
        
    return os.path.join(base_path, "Images", filename)

def Capture():
    return pyautogui.screenshot()

def SearchImage(Screenshot, image_path, confidence=0.85):
    try:
        screenshot_np = np.array(Screenshot)
        screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)
        screen_h, screen_w = screenshot_gray.shape[:2]
        
        template_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        
        if template_gray is None:
            return None
        
        h, w = template_gray.shape
        best_match = None
        
        for scale in np.linspace(0.8, 1.2, 9):
            resized_w = int(w * scale)
            resized_h = int(h * scale)
            
            if resized_h > screen_h or resized_w > screen_w:
                continue
                
            resized_template = cv2.resize(template_gray, (resized_w, resized_h))
            result = cv2.matchTemplate(screenshot_gray, resized_template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)
            
            if best_match is None or max_val > best_match['val']:
                best_match = {
                    'val': max_val,
                    'loc': max_loc,
                    'w': resized_w,
                    'h': resized_h
                }
        
        if best_match and best_match['val'] >= confidence:
            center_x = best_match['loc'][0] + best_match['w'] // 2
            center_y = best_match['loc'][1] + best_match['h'] // 2
            return pyautogui.Point(x=center_x, y=center_y)
            
        return None
        
    except Exception:
        return None

def Menu():
    global timeSleep
    while True:
        print("\n=== Auto Accept Game ===")
        print("1. Counter-Strike 2 (CS2)")
        print("2. League of Legends (LoL)")
        print(f"3. Cambiar tiempo de espera (Actual: {timeSleep}s)")
        print("0. Salir")
        print("========================")
        
        opcion = input("Elige una opción (1, 2, 3 o 0): ")
        
        if opcion == '1':
            return "CS2/CS2.png"
        elif opcion == '2':
            return "LoL/LoL.png"
        elif opcion == '3':
            try:
                nuevo_tiempo = int(input("Ingresa el nuevo tiempo de espera en segundos: "))
                if nuevo_tiempo > 0:
                    timeSleep = nuevo_tiempo
                    save_config(timeSleep)
                    print(f"¡Listo! Tiempo actualizado y guardado a {timeSleep}s.")
                else:
                    print("Error: Ingresa un número mayor a 0.")
            except ValueError:
                print("Error: Ingresa un número entero válido.")
        elif opcion == '0':
            return None
        else:
            print("Opción inválida.")

def AcceptGame(image_filename):
    global running
    running = True

    keyboard.add_hotkey('esc', stop_program)

    image_path = get_image_path(image_filename)
    
    if not os.path.exists(image_path):
        print(f"\n[ERROR] No se encontró la imagen '{image_path}'")
        return

    image_name = os.path.splitext(os.path.basename(image_path))[0]
    
    print(f"\nBuscando referencia para {image_name}...")
    print(f"Configurado con {timeSleep}s de espera.")
    print("Presiona ESC para detener\n")
    
    while running:
        Screenshot = Capture()
        
        if not running:
            break
            
        AcceptButton = SearchImage(Screenshot, image_path)
        
        if AcceptButton:
            click_x = AcceptButton.x
            click_y = AcceptButton.y
            
            if image_name.upper() == "LOL":
                click_x += 40
                print(f"Referencia LoL detectada. Click en: X={click_x}, Y={click_y}")
            elif image_name.upper() == "CS2":
                click_x += 70
                print(f"Borde de CS2 detectado. Click en: X={click_x}, Y={click_y}")
            else:
                print(f"Botón detectado en: X={click_x}, Y={click_y}")
            
            pyautogui.click(x=click_x, y=click_y)
            print(f"Partida Aceptada. Esperando {timeSleep} segundos...")
            
            for _ in range(timeSleep):
                if not running:
                    break
                time.sleep(1)
                
def main():
    while True:
        selected_image = Menu()
        if selected_image:
            AcceptGame(selected_image)
        else:
            print("Saliendo...")
            break
    return 0

if __name__ == '__main__':
    main()
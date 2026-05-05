import pyautogui
import os
import cv2
import numpy as np
import time
import keyboard

timeSleep = 5
running = False

def stop_program():
    global running
    running = False
    print("\nDeteniendo...")

def get_image_path(filename):
    """Obtiene la ruta de una imagen específica en lugar de todas."""
    currentDirectory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(currentDirectory, "Images", filename)

def Capture():
    return pyautogui.screenshot()

def SearchImage(Screenshot, image_path, confidence=0.85):
    try:
        screenshot_np = np.array(Screenshot)
        screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)
        screen_h, screen_w = screenshot_bgr.shape[:2]
        
        template_color = cv2.imread(image_path, cv2.IMREAD_COLOR)
        template_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        
        if template_color is None:
            return None
        
        image_name = os.path.basename(image_path).upper()
        
        # --- MODO COLOR (Para CS2) ---
        if "CS2" in image_name:
            avg_color = np.mean(template_color, axis=(0, 1))
            tolerance = 20
            lower_bound = np.clip(avg_color - tolerance, 0, 255).astype(np.uint8)
            upper_bound = np.clip(avg_color + tolerance, 0, 255).astype(np.uint8)
            mask = cv2.inRange(screenshot_bgr, lower_bound, upper_bound)
            
            kernel_close = np.ones((5, 5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_close)
            
            kernel_erode = np.ones((15, 15), np.uint8)
            mask_eroded = cv2.erode(mask, kernel_erode, iterations=1)
            
            num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask_eroded, connectivity=8)
            
            for i in range(1, num_labels):
                area = stats[i, cv2.CC_STAT_AREA]
                if area > 0:
                    cx, cy = int(centroids[i][0]), int(centroids[i][1])
                    if 20 <= cx <= screen_w - 20 and 20 <= cy <= screen_h - 20:
                        return pyautogui.Point(x=cx, y=cy)
            return None
            
        # --- MODO MATCHING MULTIESCALA (Para LoL) ---
        else:
            h, w = template_gray.shape
            best_match = None
            
            # Escalado dinámico de 60% a 150% con 10 tamaños (saltos de 10%)
            for scale in np.linspace(0.6, 1.5, 10):
                resized_w = int(w * scale)
                resized_h = int(h * scale)
                
                # Evita crasheos si el escalado hace que el template sea más grande que la pantalla
                if resized_h > screen_h or resized_w > screen_w:
                    continue
                    
                # Redimensionamos el template
                resized_template = cv2.resize(template_gray, (resized_w, resized_h))
                
                # Buscamos esta nueva versión en la pantalla
                result = cv2.matchTemplate(screenshot_gray, resized_template, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, max_loc = cv2.minMaxLoc(result)
                
                # Nos guardamos el que tenga la mejor coincidencia
                if best_match is None or max_val > best_match['val']:
                    best_match = {
                        'val': max_val,
                        'loc': max_loc,
                        'w': resized_w,
                        'h': resized_h
                    }
            
            # Si el mejor resultado superó nuestro límite de confianza
            if best_match and best_match['val'] >= confidence:
                # Calculamos el centro usando las dimensiones de la escala que funcionó
                center_x = best_match['loc'][0] + best_match['w'] // 2
                center_y = best_match['loc'][1] + best_match['h'] // 2
                return pyautogui.Point(x=center_x, y=center_y)
                
            return None
            
    except Exception as e:
        print(f"Error en SearchImage: {e}")
        return None

def Menu():
    """Muestra un menú para elegir qué juego buscar."""
    print("=== Auto Accept Game ===")
    print("1. Counter-Strike 2 (CS2)")
    print("2. League of Legends (LoL)")
    print("0. Salir")
    print("========================")
    
    while True:
        opcion = input("Elige una opción (1, 2 o 0): ")
        if opcion == '1':
            return "CS2/CS2.png"
        elif opcion == '2':
            return "LoL/LoL.png"
        elif opcion == '0':
            return None
        else:
            print("Opción inválida. Por favor ingresa 1, 2 o 0.")

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

                offset_x = 80  
                offset_y = 0
                
                click_x += offset_x
                click_y += offset_y
                print(f"Recorte de LoL encontrado. Moviendo el click a la zona roja: X={click_x}, Y={click_y}")
            else:
                print(f"Botón encontrado en X={click_x}, Y={click_y}")
            
            pyautogui.click(x=click_x, y=click_y)
            print(f"Partida Aceptada, esperando {timeSleep} segundos antes de buscar de nuevo...")
            
            for _ in range(timeSleep):
                if not running:
                    break
                time.sleep(1)
                
def main():
    selected_image = Menu()
    if selected_image:
        AcceptGame(selected_image)
    else:
        print("Saliendo del programa...")
    return 0

if __name__ == '__main__':
    main()
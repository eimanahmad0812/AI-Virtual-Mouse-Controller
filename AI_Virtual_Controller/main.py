import cv2
import pyautogui
import screen_brightness_control as sbc
import time
from gesture_engine import HandDetector

cap = cv2.VideoCapture(0)
detector = HandDetector()
sw, sh = pyautogui.size()
pyautogui.PAUSE = 0
cooldowns = {"click": 0, "google": 0, "bright": 0}

while True:
    success, img = cap.read()
    if not success: break
    img = cv2.flip(img, 1)
    detector.process_frame(img)
    lm = detector.getLandmarks()
    
    status = "IDLE"
    if lm:
        idx_up = lm[8].y < lm[6].y
        mid_up = lm[12].y < lm[10].y
        rng_up = lm[16].y < lm[14].y
        pnk_up = lm[20].y < lm[18].y

        # A. MOVE: Only Index Up
        if idx_up and not mid_up:
            pyautogui.moveTo(int(lm[8].x * sw), int(lm[8].y * sh))
            status = "MOVING"

        # B. CLICK: Pinch
        dist = ((lm[4].x - lm[8].x)**2 + (lm[4].y - lm[8].y)**2)**0.5
        if dist < 0.05 and mid_up and rng_up and pnk_up:
            if time.time() - cooldowns["click"] > 1:
                pyautogui.click()
                status = "CLICK"
                cooldowns["click"] = time.time()
        
        # C. SCROLL: Index + Middle up
        elif idx_up and mid_up and not rng_up:
            pyautogui.scroll(20)
            status = "SCROLLING"
            
        # D. GOOGLE: Middle only
        elif mid_up and not idx_up and not rng_up:
            if time.time() - cooldowns["google"] > 3:
                pyautogui.hotkey('win', 'r')
                pyautogui.typewrite('chrome https://www.google.com')
                pyautogui.press('enter')
                status = "OPENING GOOGLE"
                cooldowns["google"] = time.time()
        
        # E. BRIGHTNESS: Palm/Fist
        elif time.time() - cooldowns["bright"] > 0.5:
            if all([idx_up, mid_up, rng_up, pnk_up]):
                sbc.set_brightness(min(sbc.get_brightness()[0] + 10, 100))
                status = "BRIGHT UP"
                cooldowns["bright"] = time.time()
            elif not any([idx_up, mid_up, rng_up, pnk_up]):
                sbc.set_brightness(max(sbc.get_brightness()[0] - 10, 0))
                status = "BRIGHT DOWN"
                cooldowns["bright"] = time.time()

    cv2.putText(img, f"STATUS: {status}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("AI Controller", img)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()
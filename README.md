# AI Virtual Gesture Controller
A touchless, AI-powered system that controls your computer using hand gestures detected via your webcam.

## Features
- **Move:** Index finger up.
- **Click:** Pinch (Thumb + Index).
- **Scroll:** Index + Middle finger up.
- **Launch:** Middle finger up (Google Chrome).
- **Brightness:** Palm (Up) / Fist (Down).

## How to Install
1. Clone this repo.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt

## Math Logic
   Pinch: $\sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2} < 0.05$
   Finger Up: $y_{tip} < y_{knuckle}$

import cv2
from playsound import playsound
from kivy.app import App
from kivy.uix.button import Button
from kivy.clock import Clock

def capture_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    return frame if ret else None

def detect_closed_eyes(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    eyes_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    eyes = eyes_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in eyes:
        roi_gray = gray[y:y+h, x:x+w]
        _, thresholded = cv2.threshold(roi_gray, 127, 255, cv2.THRESH_BINARY)
        closed_eye = is_eye_closed(thresholded)
        if closed_eye:
            return True
    return False

def is_eye_closed(roi):
    # Implementar lógica para verificar se os olhos estão fechados
    # Exemplo simplificado: verifica se a maioria dos pixels são brancos
    white_pixels = cv2.countNonZero(roi)
    total_pixels = roi.size
    if white_pixels / total_pixels > 0.8:
        return True
    return False

def emit_beep():
    playsound('beep.wav')

class MyApp(App):
    def build(self):
        self.button = Button(text='Start Monitoring', on_press=self.start_monitoring)
        return self.button

    def start_monitoring(self, instance):
        self.button.disabled = True
        Clock.schedule_interval(self.monitor_eyes, 1 / 30)  # 30 frames por segundo

    def monitor_eyes(self, dt):
        frame = capture_image()
        if frame is not None:
            if detect_closed_eyes(frame):
                emit_beep()

if __name__ == '__main__':
    MyApp().run()

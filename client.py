import os
import pygame
from flask import Flask, Response, request
import threading
import time
import requests
import cv2
import numpy as np

WINDOW_WIDTH = 450
WINDOW_HEIGHT = 700
WINDOW_TITLE = "Volet Roulant"
FPS = 60

app = Flask(__name__)

shutdown_event = threading.Event()

class Main:
    def __init__(self, shutdown_event):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags=pygame.RESIZABLE)
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.shutdown_event = shutdown_event
        self.font = pygame.font.Font("monogram.ttf", round(self.window.get_width() * 0.07))
        self.font.set_bold(True)
        self.font_title = pygame.font.Font("monogram.ttf", round(self.window.get_width() * 0.175))
        self.font_title.set_bold(True)
        self.rect_descendre = pygame.rect.FRect(self.window.get_width() * 0.2, self.window.get_height() * 0.63, self.window.get_width() * 0.6, self.window.get_height() * 0.1)
        self.rect_monter = pygame.rect.FRect(self.window.get_width() * 0.2, self.window.get_height() * 0.33, self.window.get_width() * 0.6, self.window.get_height() * 0.1)
        self.rect_arreter = pygame.rect.FRect(self.window.get_width() * 0.2, self.window.get_height() * 0.48, self.window.get_width() * 0.6, self.window.get_height() * 0.1)
        self.color_basic = (237, 121, 33)
        self.color_shiny = (255, 170, 70)
        self.color_descendre = self.color_basic
        self.color_monter = self.color_basic
        self.color_arreter = self.color_basic
        self.text_descendre = self.font.render('DESCENDRE', True, (255, 255, 255))
        self.text_monter = self.font.render('MONTER', True, (255, 255, 255))
        self.text_arreter = self.font.render('ARRETER', True, (255, 255, 255))
        self.text_mon_volet = self.font_title.render('Mon Volet', True, (255, 255, 255))
        self.logo_upssitech = pygame.image.load("logo_upssitech.png")
        self.logo_upssitech = pygame.transform.smoothscale(self.logo_upssitech,
                                                     (969 * self.window.get_width() * 0.00075,
                                                      283 * self.window.get_height() * 0.0005))
        self.button_pressed = -1
        self.volet_status = "unknown"
        self.connection_status = "Déconnecté"  # Ajout de l'attribut pour l'état de connexion

    def resize(self):
        self.font = pygame.font.Font("monogram.ttf", round(self.window.get_width() * 0.07))
        self.font.set_bold(True)
        self.font_title = pygame.font.Font("monogram.ttf", round(self.window.get_width() * 0.175))
        self.font_title.set_bold(True)
        self.rect_descendre = pygame.rect.FRect(self.window.get_width() * 0.2, self.window.get_height() * 0.63, self.window.get_width() * 0.6, self.window.get_height() * 0.1)
        self.rect_monter = pygame.rect.FRect(self.window.get_width() * 0.2, self.window.get_height() * 0.33, self.window.get_width() * 0.6, self.window.get_height() * 0.1)
        self.rect_arreter = pygame.rect.FRect(self.window.get_width() * 0.2, self.window.get_height() * 0.48, self.window.get_width() * 0.6, self.window.get_height() * 0.1)
        self.text_descendre = self.font.render('DESCENDRE', True, (255, 255, 255))
        self.text_monter = self.font.render('MONTER', True, (255, 255, 255))
        self.text_arreter = self.font.render('ARRETER', True, (255, 255, 255))
        self.text_mon_volet = self.font_title.render('Mon Volet', True, (255, 255, 255))
        self.logo_upssitech = pygame.image.load("logo_upssitech.png")
        self.logo_upssitech = pygame.transform.smoothscale(self.logo_upssitech,
                                                     (969 * self.window.get_width() * 0.00075,
                                                      283 * self.window.get_height() * 0.0005))

    def run(self):
        threading.Thread(target=self.check_status_periodically, daemon=True).start()
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.input_process()
            self.update(dt)
            self.draw()
        pygame.quit()
        self.shutdown_event.set()

    def check_status_periodically(self):
        while self.running:
            self.get_status()
            time.sleep(2)  # Check every 2 seconds

    def get_status(self):
        try:
            response = requests.get('http://esp32-wifi-a63fc3ed2cd9.herokuapp.com/get_status')
            if response.status_code == 200:
                self.volet_status = response.json().get('status', 'unknown')
                self.connection_status = "Connecté au serveur"
            else:
                self.volet_status = "unknown"
                self.connection_status = "Déconnecté"
        except requests.ConnectionError as e:
            self.volet_status = "unknown"
            self.connection_status = f"Déconnecté: {str(e)}"

    def input_process(self):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                self.running = False
            elif (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN):
                if (self.rect_descendre.collidepoint(event.pos)):
                    self.rect_descendre.y += self.window.get_height() * 0.015
                    self.button_pressed = 1
                elif (self.rect_monter.collidepoint(event.pos)):
                    self.rect_monter.y += self.window.get_height() * 0.015
                    self.button_pressed = 2
                elif (self.rect_arreter.collidepoint(event.pos)):
                    self.rect_arreter.y += self.window.get_height() * 0.015
                    self.button_pressed = 3
            elif (event.type == pygame.MOUSEBUTTONUP or event.type == pygame.FINGERUP):
                if self.button_pressed == 1:
                    self.rect_descendre.y -= self.window.get_height() * 0.015
                    if self.rect_descendre.collidepoint(event.pos):
                        self.send_request('descend')
                elif self.button_pressed == 2:
                    self.rect_monter.y -= self.window.get_height() * 0.015
                    if self.rect_monter.collidepoint(event.pos):
                        self.send_request('monte')
                elif self.button_pressed == 3:
                    self.rect_arreter.y -= self.window.get_height() * 0.015
                    if self.rect_arreter.collidepoint(event.pos):
                        self.send_request('arret')
                self.button_pressed = -1
            elif (event.type == pygame.VIDEORESIZE):
                self.resize()

    def send_request(self, action: str):
        try:
            response = requests.post('http://esp32-wifi-a63fc3ed2cd9.herokuapp.com/button_pressed', data={'action': action})
            print(response.text)
            self.connection_status = "Connecté au serveur"
        except requests.ConnectionError as e:
            self.volet_status = "unknown"
            self.connection_status = f"Déconnecté: {str(e)}"
            print("Failed to connect to the server:", str(e))

    def update(self, dt: float):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.color_descendre = self.color_shiny if self.rect_descendre.collidepoint(mouse_x, mouse_y) else self.color_basic
        self.color_monter = self.color_shiny if self.rect_monter.collidepoint(mouse_x, mouse_y) else self.color_basic
        self.color_arreter = self.color_shiny if self.rect_arreter.collidepoint(mouse_x, mouse_y) else self.color_basic

    def draw(self):
        self.window.fill((43, 45, 48))
        self.window.blit(self.logo_upssitech, (self.window.get_width() * 0.5265 - self.logo_upssitech.get_width() * 0.5,
                                                    self.window.get_height() * 0.075 - self.logo_upssitech.get_height() * 0.5))
        self.window.blit(self.text_mon_volet, (self.window.get_width() * 0.5 - self.text_mon_volet.get_width() * 0.5,
                                               self.window.get_height() * 0.225 - self.text_mon_volet.get_height() * 0.5))
        pygame.draw.rect(self.window, (self.color_descendre[0] - 55, self.color_descendre[1] - 55, 0),
                         (
                             self.window.get_width() * 0.2, self.window.get_height() * 0.645,
                             self.window.get_width() * 0.6,
                             self.window.get_height() * 0.1),
                         border_radius=round(self.window.get_width() * 0.05))
        pygame.draw.rect(self.window, (self.color_monter[0] - 55, self.color_monter[1] - 55, 0),
                         (
                             self.window.get_width() * 0.2, self.window.get_height() * 0.345,
                             self.window.get_width() * 0.6,
                             self.window.get_height() * 0.1),
                         border_radius=round(self.window.get_width() * 0.05))
        pygame.draw.rect(self.window, (self.color_arreter[0] - 55, self.color_arreter[1] - 55, 0),
                         (
                             self.window.get_width() * 0.2, self.window.get_height() * 0.495,
                             self.window.get_width() * 0.6,
                             self.window.get_height() * 0.1),
                         border_radius=round(self.window.get_width() * 0.05))
        pygame.draw.rect(self.window, (140, 20, 42), (self.window.get_width() * 0.1, self.window.get_height() * 0.82,
                             self.window.get_width() * 0.8,
                             self.window.get_height() * 0.1),
                         border_radius=round(self.window.get_width() * 0.01))
        pygame.draw.rect(self.window, (255, 255, 255), (self.window.get_width() * 0.1, self.window.get_height() * 0.82,
                             self.window.get_width() * 0.8,
                             self.window.get_height() * 0.1),
                         width=round(self.window.get_width() * 0.0075),
                         border_radius=round(self.window.get_width() * 0.01))
        pygame.draw.line(self.window, (255, 255, 255),
                         (self.window.get_width() * 0.05, self.window.get_height() * 0.775),
                         (self.window.get_width() * 0.95, self.window.get_height() * 0.775),
                         round((self.window.get_height() * 0.0025)))
        pygame.draw.line(self.window, (255, 255, 255), (self.window.get_width() * 0.05, self.window.get_height() * 0.3), (self.window.get_width() * 0.95, self.window.get_height() * 0.3),round((self.window.get_height() * 0.0025)))
        pygame.draw.line(self.window, (255, 255, 255), (self.window.get_width() * 0.05, self.window.get_height() * 0.775), (self.window.get_width() * 0.95, self.window.get_height() * 0.775),round((self.window.get_height() * 0.0025)))
        self.draw_button(self.rect_descendre, self.color_descendre, self.text_descendre)
        self.draw_button(self.rect_monter, self.color_monter, self.text_monter)
        self.draw_button(self.rect_arreter, self.color_arreter, self.text_arreter)
        self.draw_status()
        pygame.display.flip()

    def draw_status(self):
        text: str = ""
        if self.volet_status == "unknown":
            text = self.connection_status
        if self.volet_status == "arret":
            text = "Le volet est arrêté."
        if self.volet_status == "descend":
            text = "Le volet descend."
        if self.volet_status == "monte":
            text = "Le volet monte."
        if self.volet_status == "ouvert":
            text = "Le volet est ouvert."
        if self.volet_status == "ferme":
            text = "Le volet est fermé."
        status_text = self.font.render(text, True, (255, 255, 255))
        self.window.blit(status_text, (self.window.get_width() * 0.5 - status_text.get_width() * 0.5,
                                       self.window.get_height() * 0.87 - status_text.get_height() * 0.5))

    def draw_button(self, rect, color, text):
        pygame.draw.rect(self.window, (color[0] - 55, color[1] - 55, 0),
                         (rect.x, rect.y + rect.height * 0.015, rect.width, rect.height),
                         border_radius=round(self.window.get_width() * 0.05))
        pygame.draw.rect(self.window, color, rect, border_radius=round(self.window.get_width() * 0.05))
        self.window.blit(text, (rect.centerx - text.get_width() * 0.5, rect.centery - text.get_height() * 0.5))

@app.route("/")
def home():
    return Response("Thank you for connecting\r\n", mimetype='text/plain')

def generate_frames(main):
    while main.running:
        frame = pygame.surfarray.array3d(main.window)
        frame = np.rot90(frame)
        frame = np.flipud(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(main_instance),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def run_flask():
    port = int(os.getenv('PORT', 8080))

    def check_shutdown():
        while not shutdown_event.is_set():
            time.sleep(0.1)
        os._exit(0)

    check_thread = threading.Thread(target=check_shutdown)
    check_thread.start()

    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

def run_pygame():
    global main_instance
    main_instance = Main(shutdown_event)
    main_instance.run()

if __name__ == "__main__":
    pygame_thread = threading.Thread(target=run_pygame)
    flask_thread = threading.Thread(target=run_flask)
    pygame_thread.start()
    flask_thread.start()
    pygame_thread.join()
    flask_thread.join()

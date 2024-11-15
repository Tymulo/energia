import time
import pygame
import random

class Time():
    def __init__(self, day, hour, minute):
        self.day = day
        self.hour = hour
        self.minute = minute

    def normalizetime(self):
        if self.minute == 60:
            self.hour += 1
            self.minute = 0
        if self.hour == 24:
            self.day += 1
            self.hour = 0

    def print_time(self):
        return f"Day: {self.day} {self.hour:02}:{self.minute:02}"

class Weather:
    def __init__(self, weather_type):
        self.type = weather_type
        self.active = False

def losuj_pogode(x, tab, old_weather):
    w = random.randint(1, 6)
    if w > x:
        n = random.randint(0, 3)
        old_weather.active = False
        tab[4].active = True
        x = 6
    else:
        x -= 1
    return x

class Elektrownia:
    def __init__(self, e_type, eko, koszt, dlugo):
        self.type = e_type
        self.active = False
        self.eko = eko
        self.koszt = koszt
        self.dlugo = dlugo

def ocen_efektywnosc(e, w):
    # Funkcja ocenia efektywność elektrowni na podstawie pogody
    effectiveness = {
        "solarna": {"sunny": 10, "windy": 6, "cloudy": 3, "rainy": 2},
        "wiatrowa": {"sunny": 5, "windy": 10, "cloudy": 7, "rainy": 5},
        "wodna": {"sunny": 4, "windy": 6, "cloudy": 7, "rainy": 9},
        "atomowa": {"sunny": 7, "windy": 7, "cloudy": 7, "rainy": 7},
        "weglowa": {"sunny": 3, "windy": 5, "cloudy": 8, "rainy": 7},
        "gazowa": {"sunny": 8, "windy": 7, "cloudy": 5, "rainy": 5},
    }
    return effectiveness[e.type][w.type]

def draw_bar(surface, x, y, width, height, value, max_value, color):
    pygame.draw.rect(surface, (255, 255, 255), (x, y, width, height), 2)  # Obramowanie paska
    pygame.draw.rect(surface, color, (x, y, (width * value) / max_value, height))  # Zapełnienie paska

def draw_button(surface, x, y, width, height, text, font, color):
    pygame.draw.rect(surface, color, (x, y, width, height))
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(text_surface, text_rect)


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    
    # Inicjalizacja obiektów
    wthr = [Weather("sunny"), Weather("cloudy"), Weather("windy"), Weather("rainy")]
    elektrownie = [
        Elektrownia("solarna", 7, 5, 8),
        Elektrownia("wiatrowa", 6, 4, 10),
        Elektrownia("wodna", 8, 6, 12),
        Elektrownia("atomowa", 5, 8, 15),
        Elektrownia("weglowa", 3, 2, 20),
        Elektrownia("gazowa", 6, 4, 18)
    ]

    cr_time = Time(0, 0, 0)
    time_speed = 2
    pause = False
    music_playing = True

    # Setup Pygame
    X, Y = 1280, 720
    white = (255, 255, 255)
    blue = (0, 0, 128)
    pygame.display.set_caption("Simulation")

    pauza = pygame.image.load("Pauza.png")
    wyjscie = pygame.image.load("Exit.png")
    wyjscie_rect = wyjscie.get_rect(center=(X//2 + 150, Y//2 + 60))
    wyjscie_clicked = False
    dzwiek = pygame.image.load("Sound.png")
    Nie_dzwiek = pygame.image.load("Not_sound.png")
    dzwiek_rect = dzwiek.get_rect(center=(X//2 - 150, Y//2 + 60))

    display_surface = pygame.display.set_mode((X, Y))
    font = pygame.font.Font('freesansbold.ttf', 18)

    pygame.mixer.music.load("muzyka.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    clock = pygame.time.Clock()
    time_counter = 0
    selected_plant = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Pauza gry
                    pause = not pause
            if event.type == pygame.MOUSEBUTTONDOWN:
                if wyjscie_rect.collidepoint(event.pos) and pause:  
                    wyjscie_clicked = True  
                elif dzwiek_rect.collidepoint(event.pos) and pause: 
                    if music_playing:
                        pygame.mixer.music.pause()
                        music_playing = False
                    else:
                        pygame.mixer.music.unpause()
                        music_playing = True
                if selected_plant is None:
                    if 50 <= event.pos[0] <= 250 and 150 <= event.pos[1] <= 200:
                        selected_plant = elektrownie[0]  # Solarna
                    elif 300 <= event.pos[0] <= 500 and 150 <= event.pos[1] <= 200:
                        selected_plant = elektrownie[1]  # Wiatrowa
                    elif 550 <= event.pos[0] <= 750 and 150 <= event.pos[1] <= 200:
                        selected_plant = elektrownie[2]  # Wodna
                    elif 800 <= event.pos[0] <= 1000 and 150 <= event.pos[1] <= 200:
                        selected_plant = elektrownie[3]  # Atomowa
                    elif 1050 <= event.pos[0] <= 1250 and 150 <= event.pos[1] <= 200:
                        selected_plant = elektrownie[4]  # Węglowa

        # Czyszczenie ekranu
        display_surface.fill(blue)

        # Zmiana czasu co 1 sekundę
        if not pause:
            time_counter += clock.get_time()  # Zliczanie czasu, w milisekundach
            if time_counter >= 1000:  # Jeżeli minęła sekunda (1000ms)
                cr_time.minute += 1
                cr_time.normalizetime()
                time_counter = 0  # Resetowanie licznika czasu
            if cr_time.minute % 10 == 0:
                current_weather = random.choice(wthr)

        # Wyświetlanie czasu i pogody
        time_text = font.render(cr_time.print_time(), True, white, blue)
        textRect = time_text.get_rect(center=(X // 2, 50))
        display_surface.blit(time_text, textRect)
        weather_text = font.render(f"Weather: {current_weather.type}", True, (255, 255, 255))
        display_surface.blit(weather_text, (50, 80))

        # Efektywność elektrowni
        if selected_plant:
            selected_plant_text = font.render(f"Wybrana Elektrownia: {selected_plant.type.capitalize()}", True, (255, 255, 255))
            display_surface.blit(selected_plant_text, (50, 200))

            # Wyliczanie wartości ekologii i reputacji
            ekologia = (selected_plant.eko + selected_plant.dlugo) / 2 * 100
            reputacja = (ocen_efektywnosc(selected_plant, current_weather) * 100) - selected_plant.koszt
            draw_bar(display_surface, 50, 250, 200, 20, ekologia, 100, (0, 255, 0))  # Ekologia
            draw_bar(display_surface, 50, 280, 200, 20, reputacja, 100, (255, 0, 0))  # Reputacja

        if selected_plant is None:
            draw_button(display_surface, 50, 150, 200, 50, "Solarna", font, (0, 128, 0))
            draw_button(display_surface, 300, 150, 200, 50, "Wiatrowa", font, (0, 0, 255))
            draw_button(display_surface, 550, 150, 200, 50, "Wodna", font, (0, 191, 255))
            draw_button(display_surface, 800, 150, 200, 50, "Atomowa", font, (255, 69, 0))
            draw_button(display_surface, 1050, 150, 200, 50, "Węglowa", font, (139, 69, 19))

        if pause:
            pauza_rect = pauza.get_rect(center=(X // 2, Y // 2))  # Wyśrodkowanie obrazu
            display_surface.blit(pauza, pauza_rect)
            display_surface.blit(wyjscie, wyjscie_rect)
            if music_playing:
                display_surface.blit(dzwiek, dzwiek_rect)
            else:
                display_surface.blit(Nie_dzwiek, dzwiek_rect)
            if wyjscie_clicked:
                running = False

        # Aktualizacja ekranu
        pygame.display.flip()
        clock.tick(30)  # Ustawienie liczby klatek na sekundę

    pygame.quit()

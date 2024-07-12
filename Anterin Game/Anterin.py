import pygame
import random
import time
import sys

pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()
CHARACTER_START_VALUE = 0
start_time = time.time()
time_left = 60 
# Membuat tampilan game dengan lebar 1400 dan tinggi 800 pixel========================
screen = pygame.display.set_mode((1400, 800))

# Memberi nama pada window game=======================================================
pygame.display.set_caption("Anterin")

# menginisiasi home===================================================================
class Home:
    def __init__(self, image, screen):
        self.image = image
        self.screen = screen
        self.width, self.height = screen.get_size()

        # Background
        self.background = pygame.image.load(image).convert()
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        # Text
        self.title_font = pygame.font.SysFont('Arial', 32)
        self.title_text = self.title_font.render('', True, (0, 0, 0))
        self.title_rect = self.title_text.get_rect(center=(self.width/2, self.height/3))

    def draw(self):
        # Background
        self.screen.blit(self.background, (0, 0))

        # Text
        self.screen.blit(self.title_text, self.title_rect)

    def set_title(self, text):
        self.title_text = self.title_font.render(text, True, (0, 0, 0))
        self.title_rect = self.title_text.get_rect(center=(self.width/2, self.height/3))

# Menginisialisasi button===========================================================
class Button:
    def __init__(self, x, y, width, height, inactive_color, active_color, text=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.text = text
        self.font = pygame.font.SysFont("Times", 60)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, self.active_color, self.rect)
        else:
            pygame.draw.rect(surface, self.inactive_color, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            return pygame.mouse.get_pressed()[0]
        return False
# Menginisialisasi customer===========================================================
class Customer:
    def __init__(self, x, y, image):
        self.image = image
        self.image = image
        self.rect = pygame.Rect(x, y, image.get_width(), image.get_height())
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def increase_value(self):
        self.value += 1

# Menginisialisasi Market==========================================================
class Market(Customer):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.active = True

# Menginisialisasi Character==========================================================
class Character:
    def __init__(self, x, y, image, screen_width, screen_height, map_data):
        self.x = x
        self.y = y
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.image = image
        self.rect = pygame.Rect(x, y, image.get_width(), image.get_height())
        self.width = self.rect.width
        self.height = self.rect.height
        self.map_data = map_data
        self.score = 0
        self.touched_market = False
        self.value = CHARACTER_START_VALUE
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, x, y):
        # kode validasi posisi baru
        new_x = self.x + x
        new_y = self.y + y
        tile_x = int(new_x / tile_size)
        tile_y = int(new_y / tile_size)

        # cek apakah karakter bisa bergerak ke posisi baru
        if self.map_data[tile_y][tile_x] == "W":
            # karakter tidak bisa menembus dinding, tidak bergerak
            return
        elif self.map_data[tile_y][tile_x] == "B":
            # karakter bergerak lambat di semak-semak
            x *= 0.5
            y *= 0.5

        # update posisi karakter
        new_x = self.x + x
        new_y = self.y + y
        if new_x < 160:
            self.x = 160
        elif new_x + self.rect.width > self.screen_width:
            self.x = self.screen_width - self.rect.width
        else:
            self.x = new_x
        if new_y < 0:
            self.y = 0
        elif new_y + self.rect.height > self.screen_height:
            self.y = self.screen_height - self.rect.height
        else:
            self.y = new_y
        self.rect.center = (self.x, self.y)
        
        if popup_1.active and self.rect.colliderect(popup_1.rect):
            self.value += 1
            popup_1.active = False
            score_text = font.render("Score: " + str(self.value), True, (255, 255, 255))

        if popup_2.active and self.rect.colliderect(popup_2.rect):
            self.value += 1
            popup_2.active = False
            score_text = font.render("Score: " + str(self.value), True, (255, 255, 255))

        if popup_3.active and self.rect.colliderect(popup_3.rect):
            self.value += 1
            popup_3.active = False
            score_text = font.render("Score: " + str(self.value), True, (255, 255, 255))

        if popup_4.active and self.rect.colliderect(popup_4.rect):
            self.value += 1
            popup_4.active = False
        score_text = font.render("Score: " + str(self.value), True, (255, 255, 255))

            
        if market.active and self.rect.colliderect(market.rect) and not self.touched_market:
            print("nilai", self.value)
            self.touched_market = True
            market.active = False
    
# Menginisialisasi Popup=============================================================
class Popup:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = pygame.Rect(x, y, image.get_width(), image.get_height())
        self.active = False
        self.timer = 0
        self.duration = random.randint(3000, 8000)  # Durasi muncul dan menghilang acak antara 1000 - 5000ms
    
    def update(self, dt, character_rect):
        # Jika popup aktif, tambahkan waktu ke timer dan cek jika sudah mencapai durasi
        if self.active:
            self.timer += dt
            if self.timer >= self.duration:
                self.active = False
                self.timer = 0
                
        # Jika popup tidak aktif, cek jika harus muncul
        else:
            if random.random() < 0.005:  # Peluang muncul 0.5% per frame
                self.active = True
                self.timer = 0
                self.duration = random.randint(3000, 8000)
                self.rect.x = self.x  # Letak muncul tetap
                self.rect.y = self.y
        
        # Cek apakah popup masih aktif dan bersentuhan dengan karakter
        if self.active and self.rect.colliderect(character_rect):
            self.active = False
        
    def draw(self, screen):
        if self.active:
            screen.blit(self.image, self.rect)

#ukuran grid untuk tile===========================================================
tile_size = 50

# Memuat resource gambar==========================================================
home_image = "home.png"
ending_image = "ending1.png"
character_image = pygame.image.load("ojek.png").convert_alpha()
market_image = pygame.image.load("market.png").convert_alpha()
customer_image = pygame.image.load("rumah.png").convert_alpha()
popup_image = pygame.image.load("popup.png").convert_alpha()
# pygame.mixer.music.load("backsound2.mp3")

# Inisiasi=======================================================================
#Button(x, y, width, height, inactive_color, active_color)
start_button = Button(620, 400, 260, 100, (255, 165, 0), (204, 85, 0), 'Start')
repeat_button = Button(540, 400, 160, 80, (0, 128, 0), (0, 255, 0), 'Repeat')
exit_button = Button(580, 400, 260, 100, (255, 0, 0), (255, 0, 0), 'Exit')
home_tampil = Home(home_image, screen)
ending_tampil = Home(ending_image, screen)
ending_tampil.set_title('')
market = Market(1180, 300, market_image)
customer_1 = Customer(0, 50, customer_image)
customer_2 = Customer(0, 250, customer_image)
customer_3 = Customer(0, 450, customer_image)
customer_4 = Customer(0, 650, customer_image)
popup_1 = Popup(100, 50, popup_image)
popup_2 = Popup(100, 250, popup_image)
popup_3 = Popup(100, 450, popup_image)
popup_4 = Popup(100, 650, popup_image)
#
font = pygame.font.Font(None, 36)
game_over = False  # tambahkan variabel game_over

# tile setup=======================================================================
tile_size = 50
tile_images = {
    "W": pygame.image.load("wall.jpg").convert(),
    "R": pygame.image.load("tile.jpg").convert(),
    "B": pygame.image.load("bush.jpg").convert()
}
# definisikan map dalam bentuk array 2D============================================
map_data = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "WBBRRRRRRRBBBBBBBBRRRRBBBRWW",
    "WBBBBRRRRRWWWWWWWWRRWRWRRRRW",
    "WBRWWRRBBBBRRRBBRRRRWRRRRRRW",
    "WBRRRRWWRRRWWRRRBBRRRWRRRRRW",
    "WBRRRRRBBBRRRRRWWWRBRRRRRRRW",
    "WBRWRRRWWWWWWRRRRRRRBRRRWWWW",
    "WBRWRBBRRRRRRRWRRRRRRBRRRRRW",
    "WBRWRWWRBBBBBRWRWWWWWRRRWWWW",
    "WBRRRWWRRRRRRRWRRRBBBBRRWWWW",
    "WBRRRBBRRWWWWRRRWWRRRRRRRRRW",
    "WBRRRRRRRRRRRRBBBRRWWRRRRRRW",
    "WBRWWWRRRBBBRRRRRRRRRRWWRRRW",
    "WBBRRRRWWRWWWWWWWWRRRRWWWRRW",
    "WBBRRWRRRBBBBBBBBRRRRBBBBRWW",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWW"]



# fungsi untuk menggambar map=====================================================
def draw_map(map_data):
    for row, tiles in enumerate(map_data):
        for col, tile in enumerate(tiles):
            tile_img = tile_images[tile]
            screen.blit(tile_img, (col*tile_size, row*tile_size))

    #memanggil fungsi popup
    dt = clock.tick(60) / 1000.0
    popup_1.update(dt, character.rect)
    popup_2.update(dt, character.rect)
    popup_3.update(dt, character.rect)
    popup_4.update(dt, character.rect)

# Memuat resource gambar==========================================================
#tak taruh sini karena map ada diatas
character = Character(1300, 550, character_image, 1400, 800, map_data)

#gameloop========================================================================
# Gameloop
start_button_active = True  # set awal start button aktif
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            pygame.quit()
            sys.exit()
            
        if start_button_active and event.type == pygame.MOUSEBUTTONDOWN:  # tambahkan kondisi jika start button masih aktif
            if start_button.is_clicked():
                start_time = time.time()
                start_button_active = False  # set start button menjadi tidak aktif

    # Menggambar tampilan Home dan button jika start button masih aktif
    if start_button_active:
        home_tampil.draw()
        start_button.draw(screen)
    else:  # jika start button tidak aktif
        # Mengatur waktu dan skor
        current_time = time.time()
        elapsed_time = current_time - start_time
        time_left = max(5 -int(elapsed_time),0)
        score_text = font.render("Score: " + str(character.value), True, (255, 255, 255))
        time_text = font.render("Time Left: " + str(time_left), True, (255, 255, 255))
        
        if time_left == 0:
            game_over = True
            screen.fill((0, 0, 0))  
            ending_tampil.draw()
            
            font = pygame.font.SysFont("Times", 50)   
            score_text = font.render("Score: " + str(character.value), True, (255, 255, 255))
            screen.blit(score_text, (643, 300))

            font = pygame.font.SysFont("Arial-Bold", 150) 
            gameover_text = font.render("Game Over ", True, (255, 255, 255))
            screen.blit(gameover_text, (440, 150))
            # Menambahkan tombol keluar
            exit_button.draw(screen)
            
            pygame.display.update()  
            
            exit_button_active = True
            # Menunggu tombol keluar ditekan
            while True:
                for event in pygame.event.get():
                    if exit_button_active and event.type == pygame.MOUSEBUTTONDOWN:
                        if exit_button.is_clicked():
                            game_over = True
                            pygame.quit()
                            sys.exit()
            
            
            time.sleep(5)  
            pygame.quit()
            sys.exit()
            
        # Keluar dari game jika player menekan tombol close
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                pygame.quit()
                sys.exit()

        # set background color
        screen.fill((0, 0, 0))

        #fungsi menggerakkan character lewat masukan keyboard panah
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            character.move(-5, 0)
        if keys[pygame.K_RIGHT]:
            character.move(5, 0)
        if keys[pygame.K_UP]:
            character.move(0, -5)
        if keys[pygame.K_DOWN]:
            character.move(0, 5)
        
        # Menggambar/memanggai Map, Class dan fungsi
        draw_map(map_data)
        character.draw(screen)
        market.draw(screen)
        customer_1.draw(screen)
        customer_2.draw(screen)
        customer_3.draw(screen)
        customer_4.draw(screen)
        popup_1.draw(screen)
        popup_2.draw(screen)
        popup_3.draw(screen)
        popup_4.draw(screen)
        screen.blit(score_text, (10, 10))
        screen.blit(time_text, (600, 10))


    pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()

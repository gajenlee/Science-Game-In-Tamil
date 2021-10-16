import os, sys, pygame, json
from random import choice,  randint



# COLORS
TITLE_COLOR = (0, 26, 59)
USER_VIEW_BAR = (4, 36, 74)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

NORMAL_RED = (208, 6, 38)
ACTIVE_RED = (255, 8, 41)

ACTIVE_BLUE = (105, 157, 255)
NORMAL_BLUE = (50, 140, 255)

ACTIVE_GREEN = (0, 194, 142)
NORMAL_GREEN = (0, 161, 120)

INFO_COLOR = (0, 42, 95)


# ELEMENTS
ELEMENT_IMAGE_OBJECT = []
ELEMENT_IMAGE_PATH = []
SPACE = 100
ELEMENT_ACIX = []
IMAGE_SIZE = 100
FPS = 60

# qus
QUS = []
QUS_RANDOM = []

# USER
PLAYER_LIFES = 5
CLICKED_IMAGES = []


class Elements(object):

    def __init__(self):
        path = os.path.join("./packges/items/image/elements/")
        for file_name in os.listdir(path):
            ELEMENT_IMAGE_OBJECT.append(pygame.image.load(os.path.join(path + file_name)))
            ELEMENT_IMAGE_PATH.append(os.path.join(path + file_name))
    
    def draw_elements(self, surface):
        for file_count in range(len(ELEMENT_IMAGE_OBJECT)):
            surface.blit(ELEMENT_IMAGE_OBJECT[file_count], (ELEMENT_ACIX[file_count][0], ELEMENT_ACIX[file_count][1]))
    
    def aixc(self):
        for element in range(len(ELEMENT_IMAGE_OBJECT)):
            if element < 7:
                x = 280 + (SPACE * element * 1.2)
                y = 400 + SPACE
            else:
                x = 490 + (SPACE * (element - 7) * 1.5)
                y = 420 + SPACE * 2
            ELEMENT_ACIX.append([x, y, element])

class GameThings(object):
    def init(self, surface):
        self.surface = surface
        pygame.draw.rect(surface, TITLE_COLOR, (0, 0, surface.get_width(), 50))
        pygame.draw.rect(surface, USER_VIEW_BAR, (100, (surface.get_height() - 50)//2 - 120, surface.get_width() - 200, 150), border_radius=10)
        pygame.draw.rect(surface, USER_VIEW_BAR, (surface.get_width() // 2 - 425, (surface.get_height() - 50 // 2 - 300), surface.get_width() - 500, 300), border_radius=10)

    def make_button(self, surface, msg, pos_x, pos_y, width, height, normalColor, activeColor, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if pos_x + width >= mouse[0] >= pos_x and pos_y + height >= mouse[1] >= pos_y:
            pygame.draw.rect(surface, activeColor, (pos_x, pos_y, width, height))
            pygame.draw.rect(surface, ACTIVE_BLUE, (pos_x, pos_y, width, height), 3)

            if click[0] == 1 and action != None:
                action()
        
        else:
            pygame.draw.rect(surface, normalColor, (pos_x, pos_y, width, height))
        
        self.normal_text(surface, msg, WHITE, 25, (pos_x + (width // 2)), (pos_y + (height // 2)))
    
    def make_button_icon(self, surface, image, pos_x, pos_y, width, height, normalColor, activeColor, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if pos_x + width >= mouse[0] >= pos_x and pos_y + height >= mouse[1] >= pos_y:
            pygame.draw.rect(surface, activeColor, (pos_x, pos_y, width, height), border_radius= 10)

            if click[0] == 1 and action != None:
                action()
        
        else:
            pygame.draw.rect(surface, normalColor, (pos_x, pos_y, width, height))
        
        image = pygame.image.load(image)
        rect = image.get_rect()
        rect.center = ((pos_x + (width // 2)), (pos_y + (height // 2)))
        surface.blit(image, rect)

    def text_object(self, text, font, color):
        text = font.render(text, True, color)
        return text, text.get_rect()
    
    def normal_text(self, surface, text, color, size, pos_x, pos_y, fontPath = None):
        if fontPath != None:
            myFont = pygame.font.Font(fontPath, size)
        else:
            myFont = pygame.font.Font("packges/items/font/english/Catamaran-Black.ttf", size)
        
        textSurface, textRect = self.text_object(text, myFont, color)
        textRect.center = (pos_x, pos_y)
        surface.blit(textSurface, textRect)


class Display(object):

    clicked = False
    layout = 2
    life = 5

    score = 0
    
    draw_images = []
    draw_image_paths = []

    win_addtion = []

    level = 1


    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(True)

        self.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Element Finder")

        self.viewing_value_one = [self.display.get_width() // 2 - 100, self.display.get_height() // 2 - 120]
        self.viewing_value_two = [self.display.get_width() // 2, self.display.get_height() // 2 - 120]

        self.bg = pygame.image.load("./packges/items/image/bg.jpg")

        self.tamil_font = "packges/items/font/tamil/baamini.ttf"
        
        self.things = GameThings()
        
        # Clock
        self.clock = pygame.time.Clock()


        self.game_startter()

    
    def game_startter(self):
        run = True

        while run:
            self.display.blit(self.bg, (0, 0))
            self.make_button_icon_msg(self.display, "packges/items/image/icon/cil-x.png", "Exit", self.display.get_width()//2 - 100 , self.display.get_height() - 200, 100, 40, NORMAL_RED, ACTIVE_RED, self.exit)
            self.make_button_icon_msg(self.display, "packges/items/image/icon/cil-media-play.png", "Play", self.display.get_width()//2 + 10 , self.display.get_height() - 200, 100, 40, NORMAL_GREEN, ACTIVE_GREEN, self.game_loop)
            self.things.normal_text(self.display, "NrHitfs;", WHITE, 120, self.display.get_width()//2 , self.display.get_height()//2 - 50, "packges\\items\\font\\tamil\\baamini.ttf")
            self.things.normal_text(self.display, "tpisahl;il njhlq;f gr;ir epw nghj;jhid mOj;jTk;", WHITE, 50, self.display.get_width()//2, self.display.get_height() - 300, "packges\\items\\font\\tamil\\baamini.ttf")
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()
            
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.game_loop()
                    
                    if event.key == pygame.K_ESCAPE:
                        self.exit()
            
            pygame.display.update()
            self.clock.tick(FPS - 30)

    def update_qus(self):
        with open("ElementConntion.json") as file:
            data = json.load(file)
        for name in data:
            QUS.append(name)
    
    def update_random_qus(self):
        rendom_qus = choice(QUS)
        if QUS_RANDOM != []:
            for _ in range(len(QUS)):
                if rendom_qus not in QUS_RANDOM:
                    QUS_RANDOM.append(rendom_qus)
                    return rendom_qus
                rendom_qus = choice(QUS)
            else:
                self.update_random_qus()

    def game_loop(self):


        ELEMENT_IMAGE_OBJECT.clear()
        ELEMENT_IMAGE_PATH.clear()

        element_obj = Elements()
        element_obj.aixc()

        if QUS == []:
            self.update_qus()

        QUS_RANDOM.clear()
        self.rendom_qus = choice(QUS)
        if QUS_RANDOM == []:
            QUS_RANDOM.append(self.rendom_qus)
        
        
        self.level = 1
        self.start_time = pygame.time.get_ticks()

        while True:
            self.display.blit(self.bg, (0, 0))
            self.things.init(self.display)
            element_obj.draw_elements(self.display)
            self.things.make_button_icon(self.display, "packges/items/image/icon/cil-x.png", self.display.get_width() - 40,  10, 30, 30, TITLE_COLOR, ACTIVE_RED, self.exit)
            
            # Show Life
            if self.life == 1:
                pygame.draw.rect(self.display, INFO_COLOR, (self.display.get_width() - 270, 10, 150, 30), border_radius=10)
                self.things.normal_text(self.display, "re;jHgk;: " + str(self.life), ACTIVE_RED, 25, self.display.get_width() - 200, 25, self.tamil_font)
            else:
                pygame.draw.rect(self.display, INFO_COLOR, (self.display.get_width() - 270, 10, 150, 30), border_radius=10)
                self.things.normal_text(self.display, "re;jHgk;: " + str(self.life), WHITE, 25, self.display.get_width() - 200, 25, self.tamil_font)

            # level
            pygame.draw.rect(self.display, INFO_COLOR, (self.display.get_width() - 470, 10, 150, 30), border_radius=10)
            self.things.normal_text(self.display, "NrHit: " + str(self.level), WHITE, 25, self.display.get_width() - 400, 25, self.tamil_font)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicked = True
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.game_end()

            for acix in ELEMENT_ACIX:
                self.mouse_hover(acix[0], acix[1])

            if self.clicked:
                for acix in ELEMENT_ACIX:
                    self.mouse_hit(acix[0], acix[1], acix[-1])    
                self.clicked = False

            # Won
            self.find_winer()

            # Qus
            self.things.normal_text(self.display, self.rendom_qus, WHITE, 50, self.display.get_width() // 2, self.display.get_height() // 2 - 200, self.tamil_font)
            try:
                self.display.blit(self.draw_images[-2], (self.viewing_value_one[0], self.viewing_value_one[1]))
                self.display.blit(self.draw_images[-1], (self.viewing_value_two[0], self.viewing_value_two[1]))
                

                with open("ElementConntion.json") as file:
                    data = json.load(file)
                
                if data[self.rendom_qus] == self.draw_image_paths:
                
                    self.draw_image_paths.clear()
                    self.draw_images.clear()
                    self.level += 1
                
                    self.rendom_qus = self.update_random_qus()

                else:
                    self.draw_images.clear()
                    self.draw_image_paths.clear()
                    self.life -= 1
                
            except:
                if self.draw_images != []:
                    self.display.blit(self.draw_images[-1], (self.viewing_value_one[0], self.viewing_value_one[1]))
            
            if self.life == 0:
                self.game_end()
            
            
            self.currect_time = ((pygame.time.get_ticks() - self.start_time) // 1000)
            pygame.draw.rect(self.display, INFO_COLOR, (30, 10, 150, 30), border_radius=10)
            self.things.normal_text(self.display, "Neuk;: " + str(self.currect_time), WHITE, 25, 100, 25, self.tamil_font)
                

            pygame.display.update()
            self.clock.tick(FPS)

    
    def find_winer(self):
        with open("ElementConntion.json") as file:
                data = json.load(file)
        if len(data) == len(QUS_RANDOM):
            self.show_winer_text()

    def show_winer_text(self):
        while True:
            self.display.blit(self.bg, (0, 0))
            self.make_button_icon_msg(self.display, "packges/items/image/icon/cil-x.png", "Exit", self.display.get_width()//2 - 100 , self.display.get_height() - 200, 100, 40, NORMAL_RED, ACTIVE_RED, self.exit)
            self.make_button_icon_msg(self.display, "packges/items/image/icon/cil-reload.png", "Play", self.display.get_width()//2 + 10 , self.display.get_height() - 200, 100, 40, NORMAL_GREEN, ACTIVE_GREEN, self.rerun_game_loop)
            self.things.normal_text(self.display, "ePq;fs; jhd; Ntw;wpahsH", ACTIVE_GREEN, 100, self.display.get_width() // 2, self.display.get_height() - 400, self.tamil_font)
            self.things.normal_text(self.display, "vLj;Jf;nfhz;l Neuk;: " + str(self.currect_time) + " tpdhbfs;", WHITE, 30, self.display.get_width() // 2, self.display.get_height() - 300, self.tamil_font)

            if self.currect_time <= 20:
                self.things.normal_text(self.display, "gFg;gha;T: kpfTk; ey;yJ ", ACTIVE_GREEN, 30, self.display.get_width() // 2, self.display.get_height() - 250, self.tamil_font)
            
            elif self.currect_time >= 20 and self.currect_time <= 40:
                self.things.normal_text(self.display, "gFg;gha;T: ey;yJ ", ACTIVE_GREEN, 30, self.display.get_width() // 2, self.display.get_height() - 250, self.tamil_font)
            
            elif self.currect_time >= 40 and self.currect_time <= 50:
                self.things.normal_text(self.display, "gFg;gha;T: Kaw;rp Njit ", WHITE, 30, self.display.get_width() // 2, self.display.get_height() - 250, self.tamil_font)

            else:
                self.things.normal_text(self.display, "gFg;gha;T: kpfTk; Kaw;rp Njit ", ACTIVE_RED, 30, self.display.get_width() // 2, self.display.get_height() - 250, self.tamil_font)



            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.rerun_game_loop()
                    
            pygame.display.update()
        
    
    def show_correct_incorrect(self, msg):
        self.display.blit(self.bg, (0, 0))
        self.things.normal_text(self.display, msg, WHITE, 50, self.display.get_width() // 2, self.display.get_height() - 400, self.tamil_font)



    def mouse_hit(self, xpos, ypos, index):
        mouse = pygame.mouse.get_pos()
        if (xpos + IMAGE_SIZE) >= mouse[0] >= xpos and (ypos + IMAGE_SIZE) >= mouse[1] >= ypos:
            pygame.draw.rect(self.display, ACTIVE_BLUE, (xpos, ypos, 100, 100), 4, border_radius=20)
            if self.draw_images != []:
                if ELEMENT_IMAGE_OBJECT[index] not in self.draw_images:
                    self.draw_images.append(ELEMENT_IMAGE_OBJECT[index])
                    self.draw_image_paths.append(ELEMENT_IMAGE_PATH[index])
                if len(self.draw_images) >= 3:
                    self.draw_images.clear()
                    self.draw_image_paths.clear()
            else:
                self.draw_images.append(ELEMENT_IMAGE_OBJECT[index])
                self.draw_image_paths.append(ELEMENT_IMAGE_PATH[index])


    def check_images(self, element_list:list, user_element:list) -> bool:
        for elem in element_list:
            if elem == user_element:
                return True
        return False

    def mouse_hover(self, xpos, ypos):
        mouse = pygame.mouse.get_pos()
        if (xpos + IMAGE_SIZE) >= mouse[0] >= xpos and (ypos + IMAGE_SIZE) >= mouse[1] >= ypos:
            pygame.draw.rect(self.display, NORMAL_BLUE, (xpos, ypos, 100, 100), 4, border_radius=20)
        
    
    def exit(self):
        pygame.quit()
        sys.exit()

    def make_button_icon_msg(self, surface, image, msg, pos_x, pos_y, width, height, normalColor, activeColor, action=None):
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if pos_x + width >= mouse[0] >= pos_x and pos_y + height >= mouse[1] >= pos_y:
                pygame.draw.rect(surface, activeColor, (pos_x, pos_y, width, height), border_radius= 15)

                if click[0] == 1 and action != None:
                    action()
            
            else:
                pygame.draw.rect(surface, normalColor, (pos_x, pos_y, width, height), 3, border_radius=15)
            
            image = pygame.image.load(image)

            myFont = pygame.font.Font("packges/items/font/english/Catamaran-Black.ttf", 25)
            textSurface, textRect =  myFont.render(msg, True, WHITE) , myFont.render(msg, True, WHITE).get_rect()
            textRect.center = (pos_x + (width // 2) + 13), (pos_y + (height // 2))
            surface.blit(textSurface, textRect)
            surface.blit(image, (pos_x + (width // 2) - 45,  pos_y + (height // 2) - 10))

    def game_end(self):
        while True:
            self.display.blit(self.bg, (0, 0))
            self.make_button_icon_msg(self.display, "packges/items/image/icon/cil-x.png", "Exit", self.display.get_width()//2 - 100 , self.display.get_height() - 200, 100, 40, NORMAL_RED, ACTIVE_RED, self.exit)
            self.make_button_icon_msg(self.display, "packges/items/image/icon/cil-reload.png", "Play", self.display.get_width()//2 + 10 , self.display.get_height() - 200, 100, 40, NORMAL_GREEN, ACTIVE_GREEN, self.rerun_game_loop)
            self.things.normal_text(self.display, "Ml;lk; Kbe;jJ.....", ACTIVE_RED, 100, self.display.get_width() // 2, self.display.get_height() - 400, self.tamil_font)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.rerun_game_loop()
                    
            pygame.display.update()
            self.clock.tick(FPS - 30)

    def rerun_game_loop(self):
        self.life = 5
        self.game_loop()
        


if __name__ == "__main__":
    Display()

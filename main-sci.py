import os, sys, pygame, json

from pygame import mouse

# COLORS
BG_COLOR = (30, 30, 30)
TITLE_COLOR = (44, 44, 44)
USER_VIEW_BAR = (50, 50, 50)

WHITE = (255, 255, 255)
BLACK = (0, 0, )

NORMAL_RED = (208, 6, 38)
ACTIVE_RED = (255, 8, 41)
ACTIVE_BLUE = (105, 157, 255)
NORMAL_BLUE = (50, 140, 255)

# ELEMENTS
ELEMENT_IMAGE_OBJECT = []
ELEMENT_IMAGE_PATH = []
SPACE = 100
ELEMENT_ACIX = []
IMAGE_SIZE = 100
FPS = 60

# USER
PLAYER_LIFES = 5
CLICKED_IMAGES = []


class Elements(object):

    def __init__(self):
        path = os.path.join("./packges/items//image/elements/")
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
    def __init__(self, surface):
        self.surface = surface
        pygame.draw.rect(surface, TITLE_COLOR, (0, 0, surface.get_width(), 50))
        pygame.draw.rect(surface, USER_VIEW_BAR, (100, (surface.get_height() - 50)//2 - 120, surface.get_width() - 200, 150), border_radius=10)
        pygame.draw.rect(surface, USER_VIEW_BAR, (surface.get_width() // 2 - 425, (surface.get_height() - 50 // 2 - 300), surface.get_width() - 500, 300), border_radius=10)

    def make_button(self, surface, msg, pos_x, pos_y, width, height, normalColor, activeColor, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if pos_x + width > mouse[0] > pos_x and pos_y + height > mouse[1] > pos_y:
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

        if pos_x + width > mouse[0] > pos_x and pos_y + height > mouse[1] > pos_y:
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
            myFont = pygame.font.Font("packges/items/font/english/segoeui.ttf", size)
        
        textSurface, textRect = self.text_object(text, myFont, color)
        textRect.center = (pos_x, pos_y)
        surface.blit(textSurface, textRect)


class Display(object):

    clicked = False

    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(True)

        self.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Element Finder")

        element_obj = Elements()
        element_obj.aixc()

        while True:
            self.display.fill(BG_COLOR)
            gameThings = GameThings(self.display)
            element_obj.draw_elements(self.display)
            gameThings.make_button_icon(self.display, "packges/items/image/icon/cil-x.png", self.display.get_width() - 40, 10, 30, 30, TITLE_COLOR, ACTIVE_RED, self.exit)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicked = True

            for acix in ELEMENT_ACIX:
                self.mouse_hover(acix[0], acix[1])

            
            if self.clicked:
                mouse = pygame.mouse.get_pos()
                for acix in ELEMENT_ACIX:
                    self.mouse_hit(acix[0], acix[1])

                self.clicked = False

            pygame.display.update()
            pygame.time.delay(FPS)

    
    def mouse_hit(self, xpos, ypos):
        mouse = pygame.mouse.get_pos()
        if (xpos + IMAGE_SIZE) >= mouse[0] >= xpos and (ypos + IMAGE_SIZE) >= mouse[1] >= ypos:
            pygame.draw.rect(self.display, ACTIVE_BLUE, (xpos, ypos, 100, 100), 4, border_radius=20)

    def mouse_hover(self, xpos, ypos):
        mouse = pygame.mouse.get_pos()
        if (xpos + IMAGE_SIZE) >= mouse[0] >= xpos and (ypos + IMAGE_SIZE) >= mouse[1] >= ypos:
            pygame.draw.rect(self.display, NORMAL_BLUE, (xpos, ypos, 100, 100), 4, border_radius=20)

    
    def exit(self):
        pygame.quit()
        sys.exit()


Display()
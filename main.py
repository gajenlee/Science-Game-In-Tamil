import os
import sys
import pygame
import json

# DISPLAY SIDE
HEIGHT = 0
WIDTH = 0

# COLOR SIDE
BG_COLOR = (30, 30, 30)
NAV_BAR_COLOR = (44, 44, 44)
SHOW_EDIT = (50, 50, 50)
WHITE = (255, 255, 255)
NORMAL_CLOSE = (208, 6, 33)
ACTIVE_CLOSE = (255, 8, 41)
ACTIVE_BLUE = (105, 157, 255)

# ELEMENT SIDE
ELEMENT_IMAGE = []
ELEMENT_PATH = []
SPACE = 100
ELEMENT_X_Y = []
IMAGE_SIZE = 100

# USER SIDE
PLAYER_LIFES = 5
CLICKED_IMAGES = []
clicking_changes = 2
USER_ELEMENT_PAR = []

# ELEMENT ==> DRAW 
class Elements(object):

    def __init__(self):
        path = os.path.join("./packges/items/image/elements/")
        for file_name in os.listdir(path):
            ELEMENT_IMAGE.append(pygame.image.load(os.path.join(path + file_name)))
            ELEMENT_PATH.append(os.path.join(path  + file_name))
        print(ELEMENT_IMAGE)
        print(ELEMENT_PATH)
    
    def draw_elements(self, surface):
        for file_count in range(len(ELEMENT_IMAGE)):
            image = ELEMENT_IMAGE[file_count]
            surface.blit(image, (ELEMENT_X_Y[file_count][0], ELEMENT_X_Y[file_count][1]))
    
    def x_and_y(self):
        for element in range(len(ELEMENT_IMAGE)):
            if element < 7:
                x = 280 + (SPACE  * element * 1.2)
                y = 400 + SPACE
            else:
                x = 490 + (SPACE * (element - 7) * 1.5)
                y = 420 + SPACE * 2
            ELEMENT_X_Y.append([x, y, element])


# GAME ==> COMPONENET
class Componenet(object):
    def darw_nav_bar(self, surface):
        pygame.draw.rect(surface, NAV_BAR_COLOR, (0, 0, surface.get_width(), 50))
    
    def show_edit_bar(self, surface):
        pygame.draw.rect(surface, SHOW_EDIT, (100, (surface.get_height() - 50) // 2 - 120, surface.get_width() - 200, 150), border_radius=10)
        
    def user_face(self, surface, obj):
        pygame.draw.rect(surface, SHOW_EDIT, (surface.get_width() // 2 - 425, (surface.get_height() - 50 // 2  - 300), surface.get_width() - 500, 300), border_radius=10)
        obj.draw_elements(surface)

    def quz_display(self, surface):
        pass

    def make_button(self, surface, msg, pos_x, pos_y, width, height, normalColor, activeColor, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if pos_x + width > mouse[0] > pos_x and pos_y + height > mouse[1] > pos_y:
            pygame.draw.rect(surface, activeColor, (pos_x, pos_y, width, height), border_radius=10)

            if click[0] == 1 and action != None:
                action()
        
        else:
            pygame.draw.rect(surface, normalColor, (pos_x, pos_y, width,height), border_radius=10)

        self.normal_text(surface, msg, WHITE, 25, (pos_x + (width // 2)), (pos_y + (height // 2)))

    def text_object(self, text, font, color):
        text = font.render(text, True, color)
        return text, text.get_rect()

    def normal_text(self, surface, text, color, size, pos_x, pos_y, fontPath=None):
        if fontPath != None:
            myFont = pygame.font.Font(fontPath, size)
        else:
            myFont = pygame.font.Font("./packges/items/font/english/segoeui.ttf", size)

        textSurf, textRect = self.text_object(text, myFont, color)
        textRect.center = (pos_x, pos_y)
        surface.blit(textSurf, textRect)
        

# MAIN ==> GAME LOOP AND GAME EVENT
class Main(object):
    def __init__(self):
        global clicking_changes

        pygame.init()
        pygame.mouse.set_visible(True)

        self.display = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption(" Sicence ")

        componenet = Componenet()
        element = Elements()
        element.x_and_y()
        
        clicked = False
        show = False
        front_index = []
        back_index = []
        par = []

        while True:
            self.display.fill(BG_COLOR)
            componenet.darw_nav_bar(self.display)
            componenet.make_button(self.display, " Exit ", self.display.get_width() - 80, 10, 70, 30, NORMAL_CLOSE, ACTIVE_CLOSE, self.exit)
            componenet.normal_text(self.display, " Elements ", WHITE, 40, 100, 20)
            componenet.show_edit_bar(self.display)
            componenet.user_face(self.display, element)

            for event in  pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked = True

            if clicked:
                mouse = pygame.mouse.get_pos()
                for value in ELEMENT_X_Y:
                    if (value[0] + IMAGE_SIZE) >= mouse[0] >= value[0] and (value[1] + IMAGE_SIZE) >= mouse[1] >= value[1]:
                        pygame.draw.rect(self.display, ACTIVE_BLUE, (value[0], value[1], 100, 100), 4, border_radius=20)

                        if clicking_changes == 2:
                            par.clear()
                            with open("ElementConntion.json") as file:
                                data = json.load(file)
                            for element_list in data["Element"]:
                                if element_list[0] == ELEMENT_PATH[value[-1]]:
                                    front_index.append(value[-1])
                                    par.append(ELEMENT_PATH[value[-1]])
                                    clicking_changes -= 2

                        elif clicking_changes == 0:
                            print("click 2")
                            with open("ElementConntion.json") as file:
                                data = json.load(file)
                            for element_list in data["Element"]:
                                if element_list[-1] == ELEMENT_PATH[value[-1]]:
                                    back_index.append(value[-1])
                                    par.append(ELEMENT_PATH[value[-1]])
                                    clicking_changes = 2
                        USER_ELEMENT_PAR.append(par)
                clicked = False
            
        
            if front_index != []:
                self.display.blit(ELEMENT_IMAGE[front_index[-1]], (self.display.get_width() // 2 - 100, (self.display.get_height() - 50) // 2 - 100))

            if back_index != []:
                self.display.blit(ELEMENT_IMAGE[back_index[-1]], (self.display.get_width() // 2 , (self.display.get_height() - 50) // 2 - 100))


            if back_index != [] and front_index != []:
                with open("ElementConntion.json") as file:
                    data = json.load(file)
                for element_ in data["Element"]:
                    for us_element in USER_ELEMENT_PAR:
                        if element_ == us_element:
                            print("correct")
                else:
                    print("incorrect")

            pygame.display.update()
            pygame.time.delay(60)
    
    def exit(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main = Main()

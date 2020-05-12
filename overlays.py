import pygame
from pygame.locals import *
from game import Scene, GAME_GLOBALS
import random
import math

class Overlay():

    #Overlay class will control a surface that will be shown over another screen
    #Use case will be for a chat window where there is some complicated logic that is not necessarily used in the Game class

    def __init__(self,size,topleft):
        self.visible = False
        self.size = size
        self.surface = pygame.Surface(size)
        self.top_left = topleft
        self.focused = False

    def focused(self):
        self.focused = True

    def unfocused(self):
        self.focused = False

    def show(self):
        self.visible = True

    def display_frame(self,screen):
        screen.blit(self.surface,self.top_left)

    def process_events(self):
        if self.focused == True:
            pass

class ChatWindow(Overlay):
    def __init__(self,size,top_left):
        super().__init__(size,top_left)
        self.shifted = False
        self.restricted_keys = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        self.focused = True
        self.typying = True
        self.messages = ["Hello"]
        self.currentpending = ''

    def send_message(self):
        self.messages.append(self.currentpending)
        if len(self.messages) > 5:
            self.messages = self.messages[1:]
        self.currentpending = ''
        self.typing = False

    def process_events(self,event):
        
        if self.focused == True: 
            if self.typing == True:
                if event.type == pygame.KEYUP:
                    if event.key == K_LSHIFT or event.key == K_RSHIFT: self.shifted = False
                if event.type == pygame.KEYDOWN:
                    if event.key == K_BACKSPACE: self.currentpending = self.currentpending[:-1]
                    elif event.key == K_LSHIFT or event.key == K_RSHIFT: self.shifted = True
                    elif event.key == K_SPACE: self.currentpending += ' '
                    elif event.key == K_RETURN: self.send_message()
                    if not self.shifted:
                        if event.key == K_a and 'a' in self.restricted_keys: self.currentpending += 'a'
                        if event.key == K_b and 'b' in self.restricted_keys: self.currentpending += 'b'
                        if event.key == K_c and 'c' in self.restricted_keys: self.currentpending += 'c'
                        if event.key == K_d and 'd' in self.restricted_keys: self.currentpending += 'd'
                        if event.key == K_e and 'e' in self.restricted_keys: self.currentpending += 'e'
                        if event.key == K_f and 'f' in self.restricted_keys: self.currentpending += 'f'
                        if event.key == K_g and 'g' in self.restricted_keys: self.currentpending += 'g'
                        if event.key == K_h and 'h' in self.restricted_keys: self.currentpending += 'h'
                        if event.key == K_i and 'i' in self.restricted_keys: self.currentpending += 'i'
                        if event.key == K_j and 'j' in self.restricted_keys: self.currentpending += 'j'
                        if event.key == K_k and 'k' in self.restricted_keys: self.currentpending += 'k'
                        if event.key == K_l and 'l' in self.restricted_keys: self.currentpending += 'l'
                        if event.key == K_m and 'm' in self.restricted_keys: self.currentpending += 'm'
                        if event.key == K_n and 'n' in self.restricted_keys: self.currentpending += 'n'
                        if event.key == K_o and 'o' in self.restricted_keys: self.currentpending += 'o'
                        if event.key == K_p and 'p' in self.restricted_keys: self.currentpending += 'p'
                        if event.key == K_q and 'q' in self.restricted_keys: self.currentpending += 'q'
                        if event.key == K_r and 'r' in self.restricted_keys: self.currentpending += 'r'
                        if event.key == K_s and 's' in self.restricted_keys: self.currentpending += 's'
                        if event.key == K_t and 't' in self.restricted_keys: self.currentpending += 't'
                        if event.key == K_u and 'u' in self.restricted_keys: self.currentpending += 'u'
                        if event.key == K_v and 'v' in self.restricted_keys: self.currentpending += 'v'
                        if event.key == K_w and 'w' in self.restricted_keys: self.currentpending += 'w'
                        if event.key == K_x and 'x' in self.restricted_keys: self.currentpending += 'x'
                        if event.key == K_y and 'y' in self.restricted_keys: self.currentpending += 'y'
                        if event.key == K_z and 'z' in self.restricted_keys: self.currentpending += 'z'
                        if event.key == K_0 and '0' in self.restricted_keys: self.currentpending += '0'
                        if event.key == K_1 and '1' in self.restricted_keys: self.currentpending += '1'
                        if event.key == K_2 and '2' in self.restricted_keys: self.currentpending += '2'
                        if event.key == K_3 and '3' in self.restricted_keys: self.currentpending += '3'
                        if event.key == K_4 and '4' in self.restricted_keys: self.currentpending += '4'
                        if event.key == K_5 and '5' in self.restricted_keys: self.currentpending += '5'
                        if event.key == K_6 and '6' in self.restricted_keys: self.currentpending += '6'
                        if event.key == K_7 and '7' in self.restricted_keys: self.currentpending += '7'
                        if event.key == K_8 and '8' in self.restricted_keys: self.currentpending += '8'
                        if event.key == K_9 and '9' in self.restricted_keys: self.currentpending += '9'
                    elif self.shifted:
                        if event.key == K_a and 'A' in self.restricted_keys: self.currentpending += 'A'
                        if event.key == K_b and 'B' in self.restricted_keys: self.currentpending += 'B'
                        if event.key == K_c and 'C' in self.restricted_keys: self.currentpending += 'C'
                        if event.key == K_d and 'D' in self.restricted_keys: self.currentpending += 'D'
                        if event.key == K_e and 'E' in self.restricted_keys: self.currentpending += 'E'
                        if event.key == K_f and 'F' in self.restricted_keys: self.currentpending += 'F'
                        if event.key == K_g and 'G' in self.restricted_keys: self.currentpending += 'G'
                        if event.key == K_h and 'H' in self.restricted_keys: self.currentpending += 'H'
                        if event.key == K_i and 'I' in self.restricted_keys: self.currentpending += 'I'
                        if event.key == K_j and 'J' in self.restricted_keys: self.currentpending += 'J'
                        if event.key == K_k and 'K' in self.restricted_keys: self.currentpending += 'K'
                        if event.key == K_l and 'L' in self.restricted_keys: self.currentpending += 'L'
                        if event.key == K_m and 'M' in self.restricted_keys: self.currentpending += 'M'
                        if event.key == K_n and 'N' in self.restricted_keys: self.currentpending += 'N'
                        if event.key == K_o and 'O' in self.restricted_keys: self.currentpending += 'O'
                        if event.key == K_p and 'P' in self.restricted_keys: self.currentpending += 'P'
                        if event.key == K_q and 'Q' in self.restricted_keys: self.currentpending += 'Q'
                        if event.key == K_r and 'R' in self.restricted_keys: self.currentpending += 'R'
                        if event.key == K_s and 'S' in self.restricted_keys: self.currentpending += 'S'
                        if event.key == K_t and 'T' in self.restricted_keys: self.currentpending += 'T'
                        if event.key == K_u and 'U' in self.restricted_keys: self.currentpending += 'U'
                        if event.key == K_v and 'V' in self.restricted_keys: self.currentpending += 'V'
                        if event.key == K_w and 'W' in self.restricted_keys: self.currentpending += 'W'
                        if event.key == K_x and 'X' in self.restricted_keys: self.currentpending += 'X'
                        if event.key == K_y and 'Y' in self.restricted_keys: self.currentpending += 'Y'
                        if event.key == K_z and 'Z' in self.restricted_keys: self.currentpending += 'Z'
                        if event.key == K_0 and '0' in self.restricted_keys: self.currentpending += ')'
                        if event.key == K_1 and '1' in self.restricted_keys: self.currentpending += '!'
                        if event.key == K_2 and '2' in self.restricted_keys: self.currentpending += '@'
                        if event.key == K_3 and '3' in self.restricted_keys: self.currentpending += '#'
                        if event.key == K_4 and '4' in self.restricted_keys: self.currentpending += '$'
                        if event.key == K_5 and '5' in self.restricted_keys: self.currentpending += '%'
                        if event.key == K_6 and '6' in self.restricted_keys: self.currentpending += '^'
                        if event.key == K_7 and '7' in self.restricted_keys: self.currentpending += '&'
                        if event.key == K_8 and '8' in self.restricted_keys: self.currentpending += '*'
                        if event.key == K_9 and '9' in self.restricted_keys: self.currentpending += '('                                                                                  
            elif self.typing == False:
                if event.key == K_RETURN: self.typing = True


    def show_messages(self):
        font = pygame.font.Font(None,15)
        text = font.render(self.currentpending,True,(0,255,255))
        self.surface.blit(text,(self.surface.get_width()/2,self.surface.get_height()-20))

        for message_num in range(0,len(self.messages)):
            message = self.messages[message_num]
            font = pygame.font.Font(None,15)
            text = font.render(message,True,(255,255,255))
            self.surface.blit(text,(self.surface.get_width()/2,20*(message_num+1)))

    def display_frame(self, screen):
        self.surface.fill((0,0,0))
        self.show_messages()
        screen.blit(self.surface,self.top_left)
        


class RollDice(Overlay):
    def __init__(self,size,topleft):
        super().__init__(size,topleft)
        self.dice1 = 1
        self.dice2 = 1
        self.visible = False
        self.frame = 0
        self.surface = None

    def process_events(self):
        pass

    def display_frame(self,screen):
        self.surface.fill((62,150,81))
        if self.frame < 180:
            d1,d2 = self.rolls[math.floor(self.frame/30)]
            self.display_dice(d1,d2)
        else:
            d1 = self.dice1
            d2 = self.dice2
            self.display_dice(d1,d2)
            self.display_text(d1+d2,min(self.size))
        screen.blit(self.surface,self.top_left)

    def run_logic(self):
        if self.frame > 300:
            self.visible = False
            self.frame = 0
        elif self.visible:
            self.frame += 1

    def start_rolling(self,d1,d2):
        if self.frame == 0 and not self.visible:
            self.surface = pygame.Surface(self.size)
            self.surface.set_alpha(255)
            self.dice1 = d1
            self.dice2 = d2
            self.visible = True

            self.rolls = [(0,0)] * 5
            for randomrollnum in range(0,len(self.rolls)):
                d1 = random.randint(1,6)
                d2 = random.randint(1,6)
                self.rolls[randomrollnum] = (d1,d2)
            self.rolls.append((self.dice1,self.dice2))

    def display_dice(self,dice1,dice2):

        dicenum_to_pips =   {
                            1:[(2,2)],
                            2:[(1,1),(3,3)],
                            3:[(1,1),(2,2),(3,3)],
                            4:[(1,1),(3,1),(1,3),(3,3)],
                            5:[(1,1),(3,1),(2,2),(1,3),(3,3)],
                            6:[(1,1),(3,1),(1,2),(3,2),(1,3),(3,3)]
                            }


        surf_x, surf_y = self.size
        diceside = min(surf_x/4.5, surf_y/3)

        a = surf_x/2 - 2.5*diceside/2
        b = surf_y/2 - diceside/2 

        d1_top = b
        d1_left = a
        d1_height = diceside
        d1_width = diceside

        d2_top = b
        d2_left = a + 1.5*diceside
        d2_height = diceside
        d2_width = diceside

        pygame.draw.rect(self.surface,GAME_GLOBALS.WHITE,(d1_left,d1_top,d1_width,d1_height),0)
        pygame.draw.rect(self.surface,GAME_GLOBALS.WHITE,(d2_left,d2_top,d2_width,d2_height),0)


        for inner_x,inner_y in dicenum_to_pips[dice1]:
            pygame.draw.circle(self.surface,GAME_GLOBALS.BLACK,self.piplocation(inner_x,inner_y,(d1_left,d1_top)),round(diceside/10))

        for inner_x,inner_y in dicenum_to_pips[dice2]:
            pygame.draw.circle(self.surface,GAME_GLOBALS.BLACK,self.piplocation(inner_x,inner_y,(d2_left,d2_top)),round(diceside/10))

    def piplocation(self,x,y,dicetopleft):

        surf_x, surf_y = self.size
        inner_x = min(surf_x/4.5, surf_y/3)/5 * (x+0.5)
        inner_y = min(surf_x/4.5, surf_y/3)/5 * (y+0.5)
        left, top = dicetopleft
        return int(left+inner_x), int(top+inner_y)

    def display_text(self,num,textsize):
        surf_x, surf_y = self.size
        text = str(num)

        #outer colors ---> inner colors

        colors = [pygame.Color(0,0,0,155),pygame.Color(231, 111, 81,155),pygame.Color(244, 162, 97,155),pygame.Color(233, 196, 106,155)]

        for c_int in range(0,len(colors)):
            c_textsize = (1-(c_int*0.05))*textsize
            font = pygame.font.Font(None,int(c_textsize))
            textobj = font.render(text,True,colors[c_int])
    
            x_offset = textobj.get_rect().width / 2
            y_offset = textobj.get_rect().height / 2

            self.surface.blit(textobj,(surf_x/2-x_offset,surf_y/2-y_offset))





class TestScene(Scene):
    def __init__(self):
        super().__init__()

        self.chat = ChatWindow((400,300),(0,0))
        self.dice = RollDice((random.randint(300,800),random.randint(300,800)),(0,0))
        self.chat.focused = True
        self.chat.typing = True
    

    def run_logic(self):
        if self.chat.messages[0] == "rd":
            self.dice.start_rolling(random.randint(1,6),random.randint(1,6))
        self.dice.run_logic()


    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True, self
            if self.chat.focused:
                self.chat.process_events(event)
        return False, self

    def display_frame(self, screen):
        #draw normal scene stuff
        screen.fill((255,0,0))
        #draw overlay
        self.chat.display_frame(screen)
        if self.dice.visible:
            self.dice.display_frame(screen)
        pygame.display.update()

if __name__ == "__main__":
    
    pygame.init()

    screen_size = (1200,800)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Test Chat")

    done = False
    clock = pygame.time.Clock()
    scene = TestScene()

    while not done:
        # Process events (keystrokes, mouse clicks, etc)
        done, scene = scene.process_events()

        # Update game logic
        scene.run_logic()

        # Render current frame
        scene.display_frame(screen)
        pygame.display.flip()

        #Pause for the next frame
        clock.tick(60)
    pygame.quit()

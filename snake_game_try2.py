print("Loading Packages")

import pygame
import random
import math
import time

'''initializing the screen'''
pygame.init()
WIDTH=800
HEIGHT=800
SNAKE_SIZE=10
FPS=60

screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Snake Game")
#icon=pygame.image.load("Filenamehere")
#pygame.display.set_icon("icon")
clock=pygame.time.Clock()
game_no =0
background_img=pygame.image.load("backgroundsky.jpg")
'''loading musics and sounds'''
reward_sound=pygame.mixer.Sound("score_pop.wav")
game_over_msg_sound=pygame.mixer.Sound("game_over_msg.wav")
game_over_sound=pygame.mixer.Sound("game_over.wav")
game_music=pygame.mixer.music.load("gm_music.wav")
pygame.mixer.music.play(-1)

try:
    font=pygame.font.Font("Saturday Alright.otf",35)
    game_over_font=pygame.font.Font("Saturday Alright.otf",60)
except:
    def_font=pygame.font.get_default_font()
    font=pygame.font.Font(def_font,35)
    game_over_font=pygame.font.Font(def_font,60)



class Snake():
    def __init__(self,color,speed):
        print("class initialised")
        self.color=color
        #fisrt_block_x=250
        self.body_list=[[250,150],[240,150],[230,150],[220,150],[210,150],[200,150]]
        self.head_position=self.body_list[0]
        self.direction="R"
        self.speed=speed

    def get_direction(self):
        return self.direction

    def set_direction(self,new_direction):
        self.direction= new_direction
        return 1

    def get_body_list(self):
        return self.body_list

    def get_head_position(self):
        return self.head_position

    def set_body_list(self,bodylist):
        self.body_list=bodylist
        return 1

    def get_color(self):
        return self.color

    def set_color(self,new_color):
        self.color=new_color
        return 1

    def move(self):
        '''move snake when no reward is got'''
        if self.direction=="R":
            self.head_position[0]=self.head_position[0]+self.speed

        if self.direction=="L":
            self.head_position[0]=self.head_position[0]-self.speed

        if self.direction == "U":
            self.head_position[1]= self.head_position[1] - self.speed

        if self.direction=="D":
            self.head_position[1]=self.head_position[1]+self.speed

        self.head_position= check_boundary(self.head_position)

        return 1


    def no_reward(self):
        self.body_list.insert(0,self.head_position.copy())
        self.body_list.pop()
        return 1

    def got_reward(self):
        self.body_list.insert(0, self.head_position.copy())
        return 1



def pause_game():
    pygame.event.clear()
    game_pause=True
    while game_pause:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    end_game()
                if event.key==pygame.K_SPACE:
                    pygame.mixer.music.unpause()
                    game_pause=False

    return 1

'''draw the whole snake'''
def draw_snake_and_check_game(body_list,snake_color):
    head_pos=body_list[0].copy()
    for body_piece_no in range(len(body_list)):
        body_piece = body_list[body_piece_no].copy()
        if body_piece_no>0:
            head_body_dist=math.sqrt((body_piece[0]-head_pos[0])**2+(body_piece[1]-head_pos[1])**2)
            if head_body_dist<3:
                game_over_status=True
            else:
                game_over_status=False
        pygame.draw.rect(screen, snake_color, pygame.Rect(body_piece[0], body_piece[1],2*SNAKE_SIZE ,2*SNAKE_SIZE))
        #pygame.draw.circle(screen,snake_color,(body_piece[0],body_piece[1]),SNAKE_SIZE)
    return game_over_status


'''check the boundary of points'''
def check_boundary(point):
    '''to check the boundary and correct it'''
    x_left_bound=0
    x_right_bound=WIDTH-2
    y_top_bound=0
    y_bottom_bound=HEIGHT-2

    if point[0] > x_right_bound:
        point[0] = x_left_bound
    if point[0] < x_left_bound:
        point[0] = x_right_bound
    if point[1] > y_bottom_bound:
        point[1] = y_top_bound
    if point[1] < y_top_bound:
        point[1] = y_bottom_bound
    return point


'''generates and draw a reward in a random position when called'''
def rew_generator():
    rew_pos=[random.randint(2,798),random.randint(2,798)]
    print(rew_pos)
    return  rew_pos


def game_over_msg():
    pygame.mixer.Sound.play(game_over_sound)
    game_over_running=True
    game_over_text = game_over_font.render("Game Over", True, (255, 0, 50))
    game_over_text_rect = game_over_text.get_rect()
    game_over_text_rect.center = (WIDTH// 2,HEIGHT// 2 + 50)

    score_text = font.render(f"Score :{score}", True, (0, 0, 255))
    score_text_rect = score_text.get_rect()
    score_text_rect.center = (WIDTH// 2,HEIGHT// 2)

    play_again_text = font.render("Press Space to Play Again", True, (90,7,121))
    play_again_text_rect = play_again_text.get_rect()
    play_again_text_rect.center = (WIDTH// 2,HEIGHT// 2 - 50)
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect((WIDTH // 2) - 200, HEIGHT // 2 - 75, 400, 150))
    screen.blit(game_over_text, game_over_text_rect)
    screen.blit(score_text, score_text_rect)
    screen.blit(play_again_text, play_again_text_rect)
    pygame.display.flip()



    while game_over_running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                end_game()
            if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                game()
                game_over_running=False




def end_game():
    pygame.mixer.music.stop()
    pygame.quit()
    quit()

def show_score(score):
    text=font.render(f"score :{score}",True,(25,100,80))
    textRect=text.get_rect()
    textRect.center=(50,25)
    screen.blit(text,textRect)
    return 1

def game():
    global score
    global snake_speed
    print("Game starting")
    pygame.mixer.music.play(-1)
    game_over = False
    running = True
    score = 0
    snake_color=(255,0,0)
    snake_speed=20
    SPEED_CONTROLLER=10000
    TIME_LAG_CONTROL=1/40
    REW_COLOR = (0,0,255)
    REW_SIZE = 6
    rew_pos= rew_generator()
    #snake_name=f"new_snake_{game_no}"
    new_snake=Snake(snake_color,snake_speed)
    iter_no=0


    while running:
        if iter_no % SPEED_CONTROLLER==0:
            screen.fill((0,0,0))
            screen.blit(background_img,(0,0))
            show_score(score)
            pygame.draw.circle(screen,REW_COLOR,rew_pos,REW_SIZE)
            snake_dir=new_snake.get_direction()
            snake_body=new_snake.get_body_list()
            snake_head=new_snake.get_head_position()

            game_over=draw_snake_and_check_game(snake_body,snake_color)  #draw the snake and check whether game is over


            #if game_over==True:
             #   game_over_msg()
                



            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    end_game()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        end_game()
                    if event.key==pygame.K_UP and snake_dir not in ["U","D"]:
                        new_snake.set_direction("U")
                    if event.key==pygame.K_DOWN and snake_dir not in ["U","D"]:
                        new_snake.set_direction("D")
                    if event.key==pygame.K_LEFT and snake_dir not in ["L","R"]:
                        new_snake.set_direction("L")
                    if event.key==pygame.K_RIGHT and snake_dir not in ["L","R"]:
                        new_snake.set_direction("R")
                    if event.key==pygame.K_SPACE:
                        pygame.mixer.music.pause()
                        pause_game()

            pygame.event.clear()

            rew_head_dist = math.sqrt((rew_pos[0] - (snake_head[0]+10)) ** 2 + (rew_pos[1] - (snake_head[1]+10)) ** 2)

            #if iter_no % SPEED_CONTROLLER==0:
            new_snake.move()
            if rew_head_dist>snake_speed:
                new_snake.no_reward()
            else:
                score +=1
                pygame.mixer.Sound.play(reward_sound)
                new_snake.got_reward()
                rew_pos=rew_generator()

            clock.tick(FPS)
            pygame.display.flip()
            time.sleep(TIME_LAG_CONTROL)

        iter_no+=1




game()





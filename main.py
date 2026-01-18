import pygame
from sys import exit
import random
#steps
#0.set plain black window
#1.put backgrd
#2.rolling backgrd
#3.flying bird
#4.set collision
#5.game menu
pygame.init()
clock=pygame.time.Clock()

#window
win_height=720
win_width=551
window=pygame.display.set_mode((win_width,win_height))

#Images
bird_images=[pygame.image.load("assets/bird_down.png"),pygame.image.load("assets/bird_mid.png"),pygame.image.load("assets/bird_up.png")]
sky_images=pygame.image.load("assets/background.png")
ground_image=pygame.image.load("assets/ground.png")
top_pipe_image=pygame.image.load("assets/pipe_top.png")
bottom_pipe_image=pygame.image.load("assets/pipe_bottom.png")
game_over_image=pygame.image.load("assets/game_over.png")
start_image=pygame.image.load("assets/start.png")
#Moving ground
scroll_speed=1
bird_start_position=(100,250)
score=0
font=pygame.font.SysFont('Segoe',26)
game_stopped=True
class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,image,pipe_type):
        pygame.sprite.Sprite.__init__(self)
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.enter=False
        self.passed=False
        self.exit=False
        self.pipe_type=pipe_type
    def update(self):
        self.rect.x-=scroll_speed
        if self.rect.x<=-win_width:
            self.kill()

        global score
        if self.pipe_type=='bottom':
            if bird_start_position[0]>self.rect.topleft[0] and not self.passed:
                self.enter=True
            if bird_start_position[0]<self.rect.topright[0] and not self.passed:
                self.exit=True
            if self.enter and self.exit and not self.passed:
                self.passed=True
                score+=1

class Bird(pygame.sprite.Sprite):
    #Bird position(up-0,mid-1,down-2)->animation
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=bird_images[0]
        self.rect=self.image.get_rect()
        self.rect.center=bird_start_position
        self.image_index=0
        #flapping(-7,-3,0,3,7) by adding 0.5 for each
        self.vel=0
        self.flap=False
        self.alive=True
    def update(self,user_input):
        if self.alive:
            self.image_index+=1
        if self.image_index>=30:
            self.image_index=0
        self.image=bird_images[self.image_index //10]

        #Flapping and for gravity pull
        self.vel+=0.5
        if self.vel>7:
            self.vel=7
        if self.rect.y<500:
            self.rect.y+=int(self.vel)
        if self.vel==0:
            self.flap=False
        #Turning bird face up and down abt the dir
        self.image=pygame.transform.rotate(self.image,self.vel*-7)
        if user_input[pygame.K_SPACE] and not self.flap and self.rect.y>0 and self.alive:
            self.flap=True
            self.vel=-7
class Ground(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=ground_image
        self.rect=self.image.get_rect()
        self.rect.x,self.rect.y=x,y
    def update(self):
        self.rect.x-=scroll_speed
        if self.rect.x<=-win_width:
            self.kill()
def quit_game():
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()

def main():
    global score
    x_pos_ground,y_pos_ground=0,520
    bird=pygame.sprite.GroupSingle()
    bird.add(Bird())
    pipe_timer=0
    pipes=pygame.sprite.Group()
    ground=pygame.sprite.Group()
    ground.add(Ground(x_pos_ground,y_pos_ground))
    run=True
    while run:
        quit_game()
        window.fill((0,0,0))
        user_input=pygame.key.get_pressed()
        window.blit(sky_images, (0, 0)) #  Object,position
        if len(ground)<=2:
            ground.add(Ground(win_width,y_pos_ground)) #infinite adding of ground
        ground.draw(window)
        bird.draw(window)
        pipes.draw(window)
        score_text=font.render('Score:'+str(score),True,pygame.Color(255,255,255))
        window.blit(score_text,(20,20))
        if bird.sprite.alive:
            pipes.update()
            ground.update()

        bird.update(user_input)

        collision_pipes=pygame.sprite.spritecollide(bird.sprites()[0],pipes,False)
        collision_ground=pygame.sprite.spritecollide(bird.sprites()[0],ground,False)
        if collision_pipes or collision_ground:
            bird.sprite.alive=False
            if collision_ground:
                window.blit(game_over_image,(win_width//2-game_over_image.get_width()//2,win_height//2-game_over_image.get_height()//2))
                if user_input[pygame.K_r]:
                    score=0
                    break
        if pipe_timer<=0 and bird.sprite.alive:
            x_top,x_bottom=550,550
            y_top=random.randint(-600,-480)
            y_bottom=y_top+random.randint(98,130)+bottom_pipe_image.get_height()
            pipes.add(Pipe(x_top,y_top,top_pipe_image,'top'))
            pipes.add(Pipe(x_bottom,y_bottom,bottom_pipe_image,'bottom'))
            pipe_timer=random.randint(180,250)
        pipe_timer-=1
        clock.tick(60)
        pygame.display.update()

def menu():
    global game_stopped
    while game_stopped:
        quit_game()
        window.fill((0,0,0))
        window.blit(sky_images,(0,0))
        window.blit(ground_image,Ground(0,520))
        window.blit(bird_images[0],(100,250))
        window.blit(start_image,(win_width//2-start_image.get_width()//2,win_height//2-start_image.get_height()//2))
        user_input=pygame.key.get_pressed()
        if user_input[pygame.K_SPACE]:
            main()
        pygame.display.update()
menu()
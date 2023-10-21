from random import randint
from time import time as timer
from pygame import *

font.init()
font1=font.Font(None,80)
win=font1.render('ТЫ ВЫЙГРАЛ!',True,(255,255,255))
font2=font.Font(None,40)
mixer.init()
mixer.music.load('priroda.ogg')
mixer.music.play()
fire_sound=mixer.Sound('vistrel.ogg')
img_back='pole.png'
img_hero='ohotnik.png'
img_bullet='pula.png'
img_kam='kamen.png'
img_enemy='gus.png'
score=0
goal=20
lost=0
max_lost=10
life=3
class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        self.image=transform.scale(image.load(player_image),(size_x,size_y))
        self.speed=player_speed
        self.rect=self.image.get_rect()
        self.rect.x=player_x
        self.rect.y=player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self):
        keys=key.get_pressed()
        if keys[K_LEFT] and self.rect.x>5:
            self.rect.x-=self.speed
        if keys[K_RIGHT] and self.rect.x<win_width-80:
            self.rect.x+=self.speed
    def fire(self):
        bullet=Bullet(img_bullet,self.rect.centerx,self.rect.top,15,20,-15)
class Enemy(GameSprite):
    def update(self):
        self.rect.y+=self.speed
        global lost
        if self.rect.y>win_height:
            self.rect.x=randint(80,win_width-80)
            self.rect.y=0
            lost=lost+1
class Bullet(GameSprite):
    def update(self):
        self.rect.y+=self.speed
        if self.rect.y<0:
            self.kill()

win_width=700
win_height=500
display.set_caption('Hunting')
window = display.set_mode((win_width,win_height))
background = transform.scale(image.load(img_back),(win_width,win_height))
ohotnik=Player(img_hero,5,win_height-100,80,100,10)
gusi=sprite.Group()
for i in range(1,6):
    gus=Enemy(img_enemy,randint(80,win_width-80),-40,80,50,randint(1,5))
kamni=sprite.Group()
for i in range(1,3):
    kamen=Enemy(img_kam,randint(30,win_width-30),-40,80,50,randint(1,5))
bullets=sprite.Group()
finish=False
run=True
rel_time=False
num_fire=0
while run:
    for e in event.get():
        if e.type==QUIT:
            run=False
        elif e.type==KEYDOWN:
            if e.key==K_SPACE:
                if num_fire<5 and rel_time==False:
                    num_fire=num_fire+1
                    fire_sound.play()
                    ohotnik.fire()
                if num_fire>=5 and rel_time==False:
                    last_time=timer()
                    rel_time=True
    if not finish:
        window.blit(background,(0,0))
        ohotnik.update()
        gusi.update()
        kamni.update()
        bullets.update()
        ohotnik.reset()
        gusi.draw(window)
        kamni.draw(window)
        bullets.draw(window)
        if rel_time==True:
            now_time=timer()
            if now_time-last_time<3:
                reload=font2.render('Wait,reload...',1,(150,0,0))
                window.blit(reload,(260,460))
            else:
                num_fire=0
                rel_time=False
        collides=sprite.groupcollide(gusi,bullets,True,True)
        for c in collides:
            score=score+1
            gus=Enemy(img_enemy,randint(80,win_width-80),-40,80,50,randint(1,5))
            gusi.add(gus)
        if sprite.spritecollide(ohotnik,gusi,False) or sprite.spritecollide(ohotnik,kamni,False):
            sprite.spritecollide(ohotnik,gusi,True)
            sprite.spritecollide(ohotnik,kamni,True)
            life=life-1
        if life==0 or lost>=max_lost:
            finish=True
            window.blit(lose,(200,200))
        if score>=goal:
            finish=True
            window.blit(win,(200,200))
        text=font2.render('Добыча:'+str(score),1,(255,255,255))
        window.blit(text,(10,20))
        text_lose=font2.render('Промахи:'+str(lost),1,(255,255,255))
        window.blit(text_lose,(10,50))
        if life==3:
            life_color=(0,150,0)
        if life==2:
            life_color=(150,150,0)
        if life==1:
            life_color=(150,0,0)
        text_life=font1.render(str(life),1,life_color)
        window.blit(text_life,(650,10))
        display.update()
    else:
        finish=False
        score=0
        lost=0
        num_fire=0
        life=3
        for b in bullets:
            b.kill()
        for m in gusi:
            m.kill()
        for a in kamni:
            a.kill()
        time.delay(3000)
        for i in range(1,6):
            gus=Enemy(img_enemy,randint(80,win_width-80),-40,80,50,randint(1,5))
            gusi.add(gus)
        for i in range(1,3):
            kamen=Enemy(img_kam,randint(30,win_width-30),-40,80,50,randint(1,7))
            kamni.add(kamen)
    time.delay(60)

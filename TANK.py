
import time
import random
import math
import arcade

WIDTH = 500
HEIGHT = 500
TITLE = "TANK vs ROBOT"

class Tank(arcade.Sprite):
    def __init__(self):
        super().__init__(":resources:images/topdown_tanks/tank_red.png")
        # self.center_x = WIDTH // 2
        # self.center_y = 32
        self.center_x = WIDTH // 2
        self.center_y = HEIGHT - 50
        
        self.width = 48
        self.height = 48
        self.angle = 0
        self.change_angle = 0
        self.speed = 5
        self.bullet_list = []
        self.score = 0
        self.health = 3
        self.level = 0

    def fire(self):
        self.bullet_list.append(Bullet(self))
        self.fire_music = arcade.load_sound(":resources:sounds/hit4.wav")
        arcade.play_sound(self.fire_music)
        

    # def move(self):
    #     if self.change_angle == 1:
    #         self.angle -=2.5 
    #     elif self.change_angle == -1:
    #         self.angle +=2.5

    def rotate(self):
        self.angle -= self.change_angle * self.speed

class Enemy(arcade.Sprite):
    def __init__(self):
        super().__init__(":resources:images/animated_characters/robot/robot_climb0.png")
        #super().__init__()
        self.center_x = random.randint(0,WIDTH)#
        self.center_y = 0
        self.width = 48
        self.height = 48
        self.speed = 4
        #self.image_0 = arcade.load_texture(":resources:images/animated_characters/robot/robot_climb0.png")
        #self.image = arcade.load_texture(":resources:images/animated_characters/robot/robot_fall.png")
        
    def move(self):
        self.center_y += self.speed
        #print(self.center_y)
        # if self.center_y < 0:
        #     print("0")
        
    # def draw(self):
    #      arcade.draw_texture_rectangle(self.center_x, self.center_y, 48, 48, self.image_0)

    #def draw(self):
        #arcade.draw_texture_rectangle(self.center_x, self.center_y, 48, 48, self.image)


class Bullet(arcade.Sprite):
    def __init__(self,host):
        super().__init__(":resources:images/space_shooter/meteorGrey_tiny1.png")
        self.center_x = host.center_x
        self.center_y = host.center_y
        self.speed = 6
        self.angle = host.angle

    def move(self):
        a = math.radians(self.angle)
        self.center_x -= -self.speed * math.sin(a)
        self.center_y -= self.speed * math.cos(a)



class Game(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH,HEIGHT,TITLE,resizable=True)
        arcade.set_background_color(arcade.color.BLACK)
        self.background_image = arcade.load_texture(":resources:images/backgrounds/abstract_2.jpg")
        
        #self.score = 0
        
        self.me = Tank()
        self.it = Enemy()
#        self.tir = Bullet()
        self.enemy_list = []
        self.start_time = time.time()

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0,0,WIDTH,HEIGHT,self.background_image)
        
        # if self.it.center_y < 0:
        #     print("0")
        #     self.me.score = -1#
        # for enemy in self.enemy_list:
        #     if self.it.center_y < 0:
        #         print("0")
        #         self.me.score = -1#

        if self.me.health > 0:
            text_scor = f"score : {self.me.score}"
            arcade.draw_text(text_scor,10,5,arcade.color.BLACK,15)

            lev = f"level : {self.me.level}"
            arcade.draw_text(lev,205,5,arcade.color.BLUE,15)


            if self.me.health == 3:
                text_heal = f"health:  ❤❤❤"
            elif self.me.health == 2:
                text_heal = f"health : ❤❤"
            elif self.me.health == 1:
                text_heal = f"health : ❤"

            arcade.draw_text(text_heal,350,5,arcade.color.RED,15)

            
            # text_heal = "health: "
            # arcade.draw_text(text_heal,350,5,arcade.color.RED,15,bold=True)

            # for i in range(self.me.health):
            #     i = "❤ "
            #     #h = print(i)
            #     arcade.draw_text(i,450,5,arcade.color.RED,15)


            # #lev = "level: "
            # arcade.draw_text('level',250,50,arcade.color.BLUE,15)
            # arcade.draw_text(self.me.level,250,5,arcade.color.BLUE,15)
            

            self.me.draw()
            for enemy in self.enemy_list:
                enemy.draw()

            #self.it.draw()
            for bullet in self.me.bullet_list:
                bullet.draw()
        else:
            self.background_image = arcade.load_texture(":resources:images/backgrounds/stars.png")
            self.over_music = arcade.load_sound(":resources:sounds/gameover3.wav")
            arcade.play_sound(self.over_music)       
            arcade.pause(0.5)

            arcade.draw_text("GAME OVER!",0,250,arcade.color.RED,width=500,font_size=20,align='center')
            text_fin_score = f"score: {self.me.score}"
            arcade.draw_text(text_fin_score,0,200,arcade.color.WHITE,width=500,font_size=15,align='center') 
            #arcade.stop_sound(player)
            
            #arcade.finish_render()
            #arcade.close_window()
        
    def on_update(self, delta_time: float):
        #self.me.move()
        self.me.rotate()
        self.end_time = time.time()

        #t = random.randint(4,5)
        

        
        
        if 0 <= self.me.score < 4:
            t = random.randint(4,5)
            #print("yek")
            self.me.level = '1'
        elif 4 <= self.me.score < 7:
            t = random.randint(3,4)
            #print("do")
            self.me.level = '2'
        elif 7 <= self.me.score < 10:
            t = random.randint(2,3)
            self.me.level = '3'
            #print("se")
        else:
            t = 1
            self.me.level = 'MAX'
            #print("0")
            
        #print(t)
        if self.end_time - self.start_time > t:
            #print(str(t) + ' 0')
            self.enemy_list.append(Enemy())
            self.start_time = time.time()

        for enemy in self.enemy_list:
            enemy.move()
            
            #if enemy.center_y < 0:
            if enemy.center_y > HEIGHT:
                #print("0")
                #self.me.score -=1
                self.me.health -= 1
                self.enemy_list.remove(enemy)
                self.range_music = arcade.load_sound(":resources:sounds/error5.wav")
                arcade.play_sound(self.range_music)       

            elif arcade.check_for_collision(self.me,enemy):#
                    #self.enemy_list.remove(enemy)
                    #self.me.bullet_list.remove(bullet)
                    self.me.health = 0 
                    
            

        for bullet in self.me.bullet_list:
            bullet.move()

        for bullet in self.me.bullet_list:    
            for enemy in self.enemy_list:
                if arcade.check_for_collision(bullet, enemy):
                    #self.it.draw()
                    #enemy = arcade.load_texture(":resources:images/animated_characters/robot/robot_fall.png")
                    #enemy = arcade.load_textures(":resources:images/animated_characters/robot/robot_fall.png",0,mirrored=True)
                    #enemy = arcade.load_spritesheet(":resources:images/animated_characters/robot/robot_fall.png")
                    self.enemy_list.remove(enemy)
                    self.me.bullet_list.remove(bullet)
                    self.me.score +=1
                    self.shot_music = arcade.load_sound(":resources:sounds/hurt4.wav")
                    
                    arcade.play_sound(self.shot_music)       
                    
                # elif arcade.check_for_collision(self.me,enemy):#
                #     #self.enemy_list.remove(enemy)
                #     #self.me.bullet_list.remove(bullet)
                #     self.me.score = -1

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE:
            self.me.fire() 

        if symbol == arcade.key.RIGHT:
            #self.me.angle -= 10

            self.me.change_angle = -1
            #self.angle += self.change_angle * self.speed
            
            #self.tir.move(self)
            
        elif symbol == arcade.key.LEFT:
            #self.me.angle += 10
            
            self.me.change_angle = 1
            #self.angle += self.change_angle * self.speed

            #self.tir.move(self)

    
    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.RIGHT or arcade.key.LEFT:
            self.me.change_angle = 0

game = Game()
arcade.run()

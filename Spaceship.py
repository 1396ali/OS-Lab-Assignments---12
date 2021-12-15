import time
import random
import math
import arcade

WIDTH = 500
HEIGHT = 500
TITLE = "SPACE ✨"

class Spaceship(arcade.Sprite):
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
        self.center_x = random.randint(0,WIDTH)#
        self.center_y = 0
        self.width = 48
        self.height = 48
        self.speed = 4
        
    def move(self):
        self.center_y += self.speed
        #print(self.center_y)
        # if self.center_y < 0:
        #     print("0")
            


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
        super().__init__(WIDTH,HEIGHT,TITLE)
        arcade.set_background_color(arcade.color.BLACK)
        self.background_image = arcade.load_texture(":resources:images/backgrounds/abstract_2.jpg")
        
        #self.score = 0
        
        self.me = Spaceship()
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

        if self.me.score >=0:
            text = f"score: {self.me.score}"
            arcade.draw_text(text,200,5,arcade.color.BLACK,15,bold=True)

            self.me.draw()
            for enemy in self.enemy_list:
                enemy.draw()

            for bullet in self.me.bullet_list:
                bullet.draw()
        else:
            arcade.draw_text("GAME OVER!",0,250,arcade.color.RED,width=500,font_size=15,align='center') 
            arcade.pause(0.5)
            self.over_music = arcade.load_sound(":resources:sounds/gameover3.wav")
            player = arcade.play_sound(self.over_music)       
            #arcade.stop_sound(player)
            
            #arcade.finish_render()
            #arcade.close_window()
        
    def on_update(self, delta_time: float):
        #self.me.move()
        self.me.rotate()
        self.end_time = time.time()

        if self.end_time - self.start_time > 2:
            self.enemy_list.append(Enemy())
            self.start_time = time.time()

        for enemy in self.enemy_list:
            enemy.move()
            
            #if enemy.center_y < 0:
            if enemy.center_y > HEIGHT:
                #print("0")
                self.me.score -=1
                self.enemy_list.remove(enemy)
                self.range_music = arcade.load_sound(":resources:sounds/error5.wav")
                arcade.play_sound(self.range_music)       

            elif arcade.check_for_collision(self.me,enemy):#
                    #self.enemy_list.remove(enemy)
                    #self.me.bullet_list.remove(bullet)
                    self.me.score = -1
                    
            

        for bullet in self.me.bullet_list:
            bullet.move()

        for bullet in self.me.bullet_list:    
            for enemy in self.enemy_list:
                if arcade.check_for_collision(bullet, enemy):
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

import arcade
import math
import random
import time

WIDTH = 800
HEIGHT = 600
SIZE = 55

TITLE = "TANK vs ROBOT"

class Tank(arcade.Sprite):
    def __init__(self):
        super().__init__(":resources:images/topdown_tanks/tank_red.png")
        self.center_x = WIDTH // 2
        self.center_y = HEIGHT - 50
        self.width = SIZE
        self.height = SIZE
        self.angle = 0
        self.change_angle = 0
        self.rotate_speed = 5
        self.rocket_list = []
        self.score = 0
        self.health = 3
        self.level = 0

    def rocket(self):
        self.rocket_list.append(Rocket(self))
        self.rocket_music = arcade.load_sound(":resources:sounds/hit4.wav")
        arcade.play_sound(self.rocket_music)

    def rotate(self):
        self.angle -= self.change_angle * self.rotate_speed


class Robot(arcade.Sprite):
    def __init__(self):
        super().__init__(":resources:images/animated_characters/robot/robot_fall.png")
        self.center_x = random.randint(0,WIDTH)
        self.center_y = 0
        self.width = SIZE
        self.height = SIZE
        self.move_speed = 3
        
    def move(self):
        self.center_y += self.move_speed


class Rocket(arcade.Sprite):
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
   
        self.tank = Tank()
        self.robot = Robot()
        self.robot_list = []
        self.start_time = time.time()

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0,0,WIDTH,HEIGHT,self.background_image)

        if self.tank.health > 0:
            text_score = f"SCORE : {self.tank.score}"
            arcade.draw_text(text_score,10,5,arcade.color.PURPLE,15)

            text_level = f"LEVEL : {self.tank.level}"
            arcade.draw_text(text_level,350,5,arcade.color.BLUE,15)

            if self.tank.health == 3:
                text_heal = f"HEALTH :  ❤❤❤"
            elif self.tank.health == 2:
                text_heal = f"HEALTH : ❤❤"
            elif self.tank.health == 1:
                text_heal = f"HEALTH : ❤"

            arcade.draw_text(text_heal,625,5,arcade.color.RED,15)

            self.tank.draw()

            for robo in self.robot_list:
                robo.draw()

            for rocket in self.tank.rocket_list:
                rocket.draw()

        else:
            self.background_image = arcade.load_texture(":resources:images/backgrounds/stars.png")
            self.over_music = arcade.load_sound(":resources:sounds/gameover3.wav")
            arcade.play_sound(self.over_music)       
            arcade.pause(0.5)
            arcade.draw_text("GAME OVER!",0,350,arcade.color.RED,width=800,font_size=20,align='center')
            text_final_score = f"SCORE : {self.tank.score}"
            arcade.draw_text(text_final_score,0,300,arcade.color.WHITE,width=800,font_size=15,align='center') 
            text_final_level = f"LEVEL : {self.tank.level}"
            arcade.draw_text(text_final_level,0,250,arcade.color.GREEN,width=800,font_size=10,align='center') 
              
    def on_update(self, delta_time):
        self.tank.rotate()
        self.end_time = time.time()   
        
        if 0 <= self.tank.score < 4:
            random_time = random.randint(4,5)
            self.tank.level = 1
        elif 4 <= self.tank.score < 7:
            random_time = random.randint(3,4)
            self.tank.level = 2
        elif 7 <= self.tank.score < 10:
            random_time = random.randint(2,3)
            self.tank.level = 3
        else:
            random_time = 1
            self.tank.level = 'MAX'

        timing = self.end_time - self.start_time
        
        if timing > random_time:
            self.robot_list.append(Robot())
            self.start_time = time.time()

        for robo in self.robot_list:
            robo.move()
            
            if robo.center_y > HEIGHT:
                self.tank.health -= 1
                self.robot_list.remove(robo)
                self.range_music = arcade.load_sound(":resources:sounds/error5.wav")
                arcade.play_sound(self.range_music)       

            elif arcade.check_for_collision(self.tank,robo):
                self.tank.health = 0 
                    
        for rocket in self.tank.rocket_list:
            rocket.move()

        for rocket in self.tank.rocket_list:    
            for robo in self.robot_list:
                if arcade.check_for_collision(rocket, robo):
                    self.robot_list.remove(robo)
                    self.tank.rocket_list.remove(rocket)
                    self.tank.score +=1
                    self.shot_music = arcade.load_sound(":resources:sounds/hurt4.wav")
                    arcade.play_sound(self.shot_music)       
                    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.tank.rocket() 

        if key == arcade.key.RIGHT:
            self.tank.change_angle = -1
          
        elif key == arcade.key.LEFT:
            self.tank.change_angle = 1
    
    def on_key_release(self, key: int, modifiers: int):
        if key == arcade.key.RIGHT or arcade.key.LEFT:
            self.tank.change_angle = 0

my_game = Game()
my_game.center_window()
arcade.run()
import pygame
import sys
import numpy as np
import random
#from pygame import surface

colours = {"pink":(201, 33, 68),
    "purple":(119,84,173),
    "white":(255, 255, 255),
    "black":(0,0,0),
    "grey":(25,25,25),
    "empty":(0,0,0,0)}

start = True

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

class Screen:
    surface = 0
    s_width = 0
    s_height = 0
    font = 0
    def __init__(self, s_width, s_height, font):
        self.s_width = s_width
        self.s_height = s_height
        self.font = font
        self.surface = pygame.Surface((self.s_width, self.s_height))

    def update(self):
        pass

    def render(self):
        pass
        #pygame.draw.rect(self.surface, colours["black"], [0, 0, self.s_width, self.s_height])

class StartScreen(Screen):
    
    def __init__(self, s_width, s_height, font):
        super().__init__(s_width, s_height, font)

    def update(self):
        super().update()

    def render(self):
        super().render()
        self.surface.fill(colours["empty"])
        #print(self.font)
        pygame.draw.rect(self.surface, colours["pink"], [0,self.s_height*0.1,self.s_width*0.02, self.s_height*0.5])
        title_font = pygame.font.Font('data/MoongladeDemoBold-jOzM.ttf', 800)
        textsurface = title_font.render("The Lavender", False, colours["white"])
        self.surface.blit(textsurface, (400,  self.s_height*0.1))
        textsurface = title_font.render("Archive", False, colours["white"])
        self.surface.blit(textsurface, (400,  self.s_height*0.2))

        textsurface = self.font.render("C O L L E C T  + ", False, colours["pink"])
        self.surface.blit(textsurface, (400,  self.s_height*0.4))
        textsurface = self.font.render("P R E S E R V E ", False, colours["pink"])
        self.surface.blit(textsurface, (400,  self.s_height*0.43))

        if start:
            textsurface = self.font.render("Welcome to the Lavender Archive!", False, colours["white"])
            self.surface.blit(textsurface, (400,  self.s_height*0.62))
            textsurface = self.font.render("Due to the event that occured on the planet Erydia, we have ", False, colours["white"])
            self.surface.blit(pygame.transform.scale(textsurface, (6000, 200)), (400,  self.s_height*0.645))
            textsurface = self.font.render("been tasked to collect the final days of the planet on record.", False, colours["white"])
            self.surface.blit(pygame.transform.scale(textsurface, (6000, 200)), (400,  self.s_height*0.67))
            textsurface = self.font.render("Eventhough the Lavender Archive is equipped with the best tech,", False, colours["white"])
            self.surface.blit(pygame.transform.scale(textsurface, (6000, 200)), (400,  self.s_height*0.695))
            textsurface = self.font.render("problems are inevitable when they arise. It is your responsibility", False, colours["white"])
            self.surface.blit(pygame.transform.scale(textsurface, (6000, 200)), (400,  self.s_height*0.72))
            textsurface = self.font.render("to manage the equipment, collect and preserve the planet's", False, colours["white"])
            self.surface.blit(pygame.transform.scale(textsurface, (6000, 200)), (400,  self.s_height*0.745))
            textsurface = self.font.render("final days. To ensure you do your job, you will be required to meet", False, colours["white"])
            self.surface.blit(pygame.transform.scale(textsurface, (6000, 200)), (400,  self.s_height*0.77))
            textsurface = self.font.render("a quota every 24 hours, failure will result in your termination.", False, colours["white"])
            self.surface.blit(pygame.transform.scale(textsurface, (6000, 200)), (400,  self.s_height*0.795))
        
        else:
            textsurface = self.font.render("type \"start\" when you are ready...", False, colours["white"])
            self.surface.blit(pygame.transform.scale(textsurface, (4000, 200)), (400,  self.s_height*0.62))
        textsurface = self.font.render("type \"help\" to learn about the interface...", False, colours["white"])
        self.surface.blit(pygame.transform.scale(textsurface, (4000, 200)), (400,  self.s_height*0.845))
        return self.surface

class Grid:
    c_size = 0
    border = 0
    g_shape = (0,0)
    layer1 = np.ndarray((1,1))
    layer2 = np.ndarray((1,1))
    layer3 = np.ndarray((1,1))
    
    def __init__(self,g_shape, c_size, border):
        self.c_size = c_size
        self.border = border
        self.g_shape = g_shape
        self.layer1 = np.ndarray(g_shape).fill(2)
        self.layer2 = np.ndarray(g_shape)
        self.layer3 = np.ndarray(g_shape)

    def render(self, surface, xpos, ypos):
         for i in range(self.g_shape[0]):
            for j in range(self.g_shape[1]):
                pygame.draw.rect(surface, colours["pink"], [xpos+self.c_size*i, ypos + self.c_size*j, self.c_size+self.border, self.c_size+self.border])
                pygame.draw.rect(surface, colours["black"], [xpos+self.border+self.c_size*i, ypos+self.border + self.c_size*j, self.c_size-self.border, self.c_size-self.border])

class Reciever(Screen):
    name = ""
    map_rendered = False
    loaded = True
    load_count = 0
    load_time_tmp = 0
    receiver_cap = 1
    transmitters = ["AAAA", "BBBB", "CCCC"]
    marker_num = 5
    markers = []
    marker_level = []
    marker_pos = []
    marker_level_pool = np.concatenate((np.repeat(1, 50), np.repeat(2, 30), np.repeat(3, 15), np.repeat(4, 5)))
    selected = 0
    def drawMakerContainers(self, posx, posy, text, level, colour):
        pygame.draw.rect(self.surface, colours[colour], [posx, posy, 500, 500])
        pygame.draw.rect(self.surface, colours[colour], [posx+500, posy+50, 1200, 400])
        pygame.draw.rect(self.surface, colours["black"], [posx+50, posy+50, 400, 400])
        pygame.draw.rect(self.surface, colours["black"], [posx+500, posy+100, 1150, 300])

        textsurface = self.font.render(str(level), False, colours["white"])
        self.surface.blit(pygame.transform.scale(textsurface, (300,300)), (posx+100, posy+100))

        if len(text) > 10:
            text = text[0:7]+"..."
        textsurface = self.font.render(text, False, colours["white"])
        self.surface.blit(textsurface, (posx+600, posy+150))


    def relocateMarkers(self):
        text = np.loadtxt("data/names.txt", dtype=str,  delimiter="\n")
        for i in range(self.marker_num):
            self.markers = random.choices(text, k=self.marker_num)


    def __init__(self, s_width, s_height, font, name):
        super().__init__(s_width, s_height, font)
        self.name = name

    def update(self):
        super().update()

    def render(self):
        super().render()
        #pygame.draw.rect(self.surface, colours["pink"], [0,self.s_height*0.20, self.s_width, self.s_width*0.4])
        if not self.loaded:
            print("LOADING...")
            self.load_time_tmp += clock.tick(30)
            if self.load_time_tmp > 300:
                pygame.draw.rect(self.surface, colours["pink"], [150 + (self.load_count+1)*1000, 4000, 500, 500])
                self.load_count += 1
                self.load_time_tmp = 0
        

        if (not self.map_rendered) and self.loaded:
            #print("LOAD MAP")
            self.relocateMarkers()
            self.selected = 0
            
            self.surface.fill(colours["empty"])
            map_img = pygame.image.load("data/maps/map1.png ").convert_alpha()
            self.surface.blit(pygame.transform.scale(map_img, (int(self.s_width), int(self.s_width*0.4))), (0,int(self.s_height*0.2)))
            textsurface = self.font.render(self.name, False, colours["pink"])
            self.surface.blit(textsurface, (400,  self.s_height*0.1))
            textsurface = self.font.render(self.name, False, colours["pink"])
            self.surface.blit(textsurface, (400,  self.s_height*0.1))
            
            self.marker_pos = []
            for i in range(self.marker_num):
                self.marker_pos.append((random.randint(1500, self.s_width - 1900),  random.randint(self.s_height*0.2, self.s_width*0.4)))
                #print(self.marker_level_pool)
                self.marker_level = random.choices(self.marker_level_pool, k=self.marker_num)
            self.map_rendered = True

        if self.loaded:
            for i in range(len(self.markers)):
                if i == self.selected:
                    self.drawMakerContainers(self.marker_pos[i][0], self.marker_pos[i][1], self.markers[i], self.marker_level[i], "pink")
                else:
                    self.drawMakerContainers(self.marker_pos[i][0], self.marker_pos[i][1], self.markers[i], self.marker_level[i], "grey")
            
            pygame.draw.rect(self.surface, colours["black"], [0, 6200, self.s_width, 1000])
            textsurface = self.font.render("Name: "+self.markers[self.selected], False, colours["pink"])
            self.surface.blit(textsurface, (400,  6500))
            textsurface = self.font.render("Level: "+str(self.marker_level[self.selected]), False, colours["pink"])
            self.surface.blit(textsurface, (400,  6900))
    
        if self.load_count >= 10:
            self.loaded = True
            
            
        return self.surface

class Decoder(Screen):
    name = ""
    def __init__(self, s_width, s_height, font, name):
        super().__init__(s_width, s_height, font)
        self.name = name

    def update(self):
        super().update()

    def render(self):
        super().render()
        self.surface.fill(colours["empty"])
        textsurface = self.font.render(self.name, False, colours["pink"])
        self.surface.blit(textsurface, (400,  self.s_height*0.1))
        return self.surface


class Storage(Screen):
    cur_prob = 0
    name = ""
    

    def __init__(self, s_width, s_height, font, name):
        super().__init__(s_width, s_height, font)
        self.name = name
        self.grid = Grid((25,25), 200, 10)
    
    def update(self):
        super().update()
    
    def render(self):
        self.surface.fill(colours["empty"])
        self.grid.render(self.surface, 1000+self.cur_prob, self.s_height*0.2)
        textsurface = self.font.render(self.name, False, colours["pink"])
        self.surface.blit(textsurface, (400,  self.s_height*0.1))
        return self.surface


class Computer:
    
    font = 0
    surface = 0
    screen = 0
    screens = {}
    s_width = 0
    s_height = 0
    c_width = 0
    c_height = 0
    code = ""
    current_screen = "Reciever"
    storage_num = 3
    decoder_num = 2

    def __init__(self, c_size):
        self.c_width = c_size[0] * 10
        self.c_height = c_size[1] * 10
        self.s_width = self.c_width*0.99
        self.s_height = self.c_height*0.91
        self.surface = pygame.Surface((self.c_width, self.c_height))
        self.font = pygame.font.Font('data/SourceCodePro-Regular.ttf', self.c_height//50)

        self.screens["Start"] = StartScreen(self.s_width, self.s_height, self.font)
        self.screens["Storage 1"] = Storage(self.s_width, self.s_height, self.font, "Storage 1")
        self.screens["Storage 2"] = Storage(self.s_width, self.s_height, self.font, "Storage 2")
        self.screens["Storage 3"] = Storage(self.s_width, self.s_height, self.font, "Storage 3")
        self.screens["Decoder 1"] = Decoder(self.s_width, self.s_height, self.font, "Decoder 1")
        self.screens["Decoder 2"] = Decoder(self.s_width, self.s_height, self.font, "Decoder 2")
        self.screens["Reciever"] = Reciever(self.s_width, self.s_height, self.font, "Reciever")
        

        pygame.draw.rect(self.surface, colours["purple"], [0, 0, self.c_width, self.c_height])

    def update(self):

        for screen in self.screens:
            self.screens[screen].update()
        

    def render(self):
        pygame.draw.rect(self.surface, (0, 0, 0), [(self.c_width*0.01)/2,(self.c_height*0.01)/2, self.c_width*0.99, self.c_height*0.99])
        
        textsurface = self.font.render(">>> "+self.code, False, colours["pink"])
        self.surface.blit(textsurface, (100,  self.c_height*0.96)) 
        pygame.Surface.blit(self.surface, self.screens[self.current_screen].render(), ((self.c_width*0.01)/2,(self.c_height*0.01)/2))

        return self.surface


def main():
    global colours
    global start
    global clock

    size = w_win, h_win = 1920, 1080
    screen = pygame.display.set_mode(size)

    valid_chars = "abcdefghijklmnopqrstuvwxyz"
    valid_nums = "1234567890"
    backspace_down = False

    c_size = (1200, 800)

    computer = Computer(c_size)

    planet_frame_ctr = 1

    while (1):
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif pygame.key.name(event.key) in valid_chars+valid_nums:
                    if len(computer.code) < 45:
                        computer.code = computer.code + pygame.key.name(event.key)
                elif event.key == pygame.K_BACKSPACE:
                    backspace_down = True
                elif event.key == pygame.K_SPACE:
                    computer.code = computer.code+" "
                elif event.key == pygame.K_RETURN:
                    code_arr = computer.code.split(" ")

                    for i in code_arr:
                        if i =="":
                            code_arr.remove("")
                
                    if len(code_arr) == 1:
                        if code_arr[0] == "help":
                            computer.current_screen = "Start"
                        
                        if start:
                            if code_arr[0] == "reciever":
                                computer.current_screen = "Reciever"
                            elif code_arr[0] == "reload" and computer.current_screen == "Reciever":
                                computer.screens["Reciever"].loaded = False
                                computer.screens["Reciever"].map_rendered = False
                                computer.screens["Reciever"].load_count = 0
                                computer.screens["Reciever"].surface.fill(colours["empty"])
                        else:
                            if code_arr[0] == "start":
                                start = True
                        
                            
                    if len(code_arr) == 2 and start:
                        if code_arr[0] == "storage" and code_arr[1] in valid_nums:
                            if int(code_arr[1]) < computer.storage_num + 1:
                                computer.current_screen = "Storage "+code_arr[1]
                        
                        if code_arr[0] == "decoder" and code_arr[1] in valid_nums:
                            if int(code_arr[1]) < computer.decoder_num + 1:
                                computer.current_screen = "Decoder "+code_arr[1]
                    
                    computer.code = ""
                if start:
                    if event.key == pygame.K_RIGHT:
                        if computer.current_screen == "Reciever":
                            computer.screens["Reciever"].selected += 1
                            if computer.screens["Reciever"].selected > computer.screens["Reciever"].marker_num - 1:
                                computer.screens["Reciever"].selected = 0
                    elif event.key == pygame.K_LEFT:
                        if computer.current_screen == "Reciever":
                            computer.screens["Reciever"].selected -= 1
                            if computer.screens["Reciever"].selected < 0:
                                computer.screens["Reciever"].selected =  computer.screens["Reciever"].marker_num -1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    backspace_down = False

        if backspace_down:
            computer.code = computer.code[:-1]
        
        computer.update()



        #print("data/planet_frames/"+str(planet_frame_ctr).zfill(4)+".png ")
        planet_frame = pygame.image.load("data/planet_frames/"+str(planet_frame_ctr).zfill(4)+".png ").convert_alpha()
        planet_frame_ctr += 1
        if planet_frame_ctr > 5400:
            planet_frame_ctr = 1
        pygame.Surface.blit(screen, pygame.transform.scale(planet_frame, (1000, 1000)), (1300,-100))
        pygame.Surface.blit(screen, pygame.transform.scale(computer.render(), c_size), (20, 20))

        pygame.display.flip()


if __name__ == "__main__":
    main()

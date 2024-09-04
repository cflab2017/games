import pygame

class ShapeLoad():
    shape = {
        'color':[
                (255, 85,  85),#1
                (196, 104, 196),#2
                (120, 108, 245),#3
                (255, 140, 50),#4
                (50,  120, 52),#5
                (69, 205, 205),#6
                (150, 161, 218),#7
                (100, 161, 218),#7
                (100, 0,  100),#8
            ],
        'char':[],
        'stone':[]
        }
    
    def __init__(self,cell_size) -> None:
        self.shape['color'] = self.load_def_img(cell_size)
        self.shape['char'] = self.load_char_img(cell_size)
        self.shape['stone'] = self.load_stone_img(cell_size)
        
    def load_def_img(self,cell_size):
        file_names = [
            "def0.png", "def1.png",
            "def2.png", "def3.png",
            "def4.png", "def5.png",
            "def6.png", "def7.png",
            "boom.png",
            ]
        
        img_player = []
        for file in file_names:
            image = pygame.image.load(f"./images/{file}").convert_alpha()
            image = pygame.transform.scale(image, (cell_size, cell_size))
            img_player.append(image)  
            
        return img_player 
    
    def load_char_img(self,cell_size):
        file_names = [
            "player_army.png",    "player_dinosaur.png",
            "player_ninja.png",   "player_penguin.png",
            "player_Pirate.png",  "player_police.png",
            "player_samurai.png", "player_soldier.png",
            "boom.png",
            # "player_warrior.png",
            ]
        
        img_player = []
        for file in file_names:
            image = pygame.image.load(f"./images/{file}").convert_alpha()
            image = pygame.transform.scale(image, (cell_size, cell_size))
            img_player.append(image)  
            
        return img_player
    
    def load_stone_img(self,cell_size):
        file_names = [
            "stone0.png", "stone1.png",
            "stone2.png", "stone3.png",
            "stone4.png", "stone5.png",
            "stone6.png", "stone7.png",
            "boom.png",
            ]
        
        img_player = []
        for file in file_names:
            image = pygame.image.load(f"./images/{file}").convert_alpha()
            image = pygame.transform.scale(image, (cell_size, cell_size))
            img_player.append(image)  
            
        return img_player
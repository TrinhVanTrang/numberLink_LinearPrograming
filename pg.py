import pygame
from common import selectColors
import math

class NumberlinkUI:
    def __init__(self, w, h, N,ep,k_values,outputFile):
        self.fileOutput="output/"+outputFile
        self.end_points=ep
        self.k_values=k_values
        self.width = w
        self.height = h
        self.numColors = N
        self.colors = selectColors(N)
        pygame.init()
        self.screen_width = 720*w/15
        self.screen_height = 720*h/15
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.screen.fill("white")
        pygame.display.set_caption("Numberlink")
        self.rect_width = self.screen_width / w * 3 / 4
        self.rect_height = self.screen_height / h * 3 / 4
        
   

    def createBoard(self):
        screen = self.screen
        s_w = self.screen_width
        s_h = self.screen_height
        w = self.width
        h = self.height
        rect_width = self.rect_width
        rect_height = self.rect_height

        started_x = s_w / 4 / 2
        started_y = s_h / 4 / 2

        colors = self.colors
        color = "white"
        for i in range(w):
            for j in range(h):
                # pygame.draw.rect(
                #     screen, color, (started_x+i * rect_width, started_y+j*rect_height, rect_width, rect_height),
                # )
                pygame.draw.rect(
                    screen,
                    "black",
                    (
                        started_x + i * rect_width,
                        started_y + j * rect_height,
                        rect_width,
                        rect_height,
                    ),
                    2,
                )
                pygame.display.flip()
                # pygame.display.update()

    def showEndPoint(self):
        screen = self.screen
        end_points=self.end_points
        k_values=self.k_values
        screen = self.screen
        s_w = self.screen_width
        s_h = self.screen_height
        w = self.width
        h = self.height
        rect_width = self.rect_width
        rect_height = self.rect_height

        started_x = s_w / 4 / 2
        started_y = s_h / 4 / 2
        colors = self.colors
        size_text=int(math.sqrt(rect_height*rect_width)/2)
        font = pygame.font.Font('freesansbold.ttf', size_text)
        for ep in end_points:
            i=ep[0]-1
            j=ep[1]-1
            x = started_x + j * rect_width
            y = started_y + i * rect_height
            color = colors[k_values.index(ep[2])]
            # pygame.draw.rect(
            #         screen, color, (x, y, rect_width, rect_height),
            #     )
            text = font.render(str(ep[2]), True, 'black', color)
            textRect = text.get_rect()
            textRect.center = (x+rect_width/2,y+rect_height/2)
            screen.blit(text, textRect)
            # pygame.display.flip()
            
    def showPaths(self):
        screen = self.screen
        end_points=self.end_points
        k_values=self.k_values
        screen = self.screen
        s_w = self.screen_width
        s_h = self.screen_height
        w = self.width
        h = self.height
        rect_width = self.rect_width
        rect_height = self.rect_height

        started_x = s_w / 4 / 2
        started_y = s_h / 4 / 2
        colors = self.colors
        file=open(self.fileOutput,"r")
        
        i=0
        for line in file:
            line=line.replace('\n','')
            row=line.split(' ')
            for j in range(0,len(row)-1):
                x = started_x + j * rect_width
                y = started_y + i * rect_height
                color = colors[k_values.index(int(row[j]))]
                pygame.draw.rect(
                        screen, color, (x, y, rect_width, rect_height),
                    )
                pygame.display.flip()
            i+=1    
        file.close()

    def render(self):
        
        self.showPaths()
        self.showEndPoint()
        self.createBoard()

        running = True
        while running:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()



    
    

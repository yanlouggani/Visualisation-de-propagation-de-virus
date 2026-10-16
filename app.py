import pygame
from model import VirusSimulation
import pandas as pd
##initialisation des agents

model = VirusSimulation(height=600, width=800, n=100, infected=10,rng= 42)


pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True
font = pygame.font.Font("assets/fonts/PixeloidSans.ttf", 16)
my_text = font.render("Press SPACE to advance the simulation", True, (255, 255, 255))

while running:
    screen.fill((0, 0, 0))  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            df = model.datacollector.get_model_vars_dataframe()
            df.to_csv("outputs/simulation.csv", index=False)
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                model.step()

    step_text = [f"jour : {model.day}",f"nombre d'agents sain : {model.sain()} ",f"nombre d'infectés : {model.infected()} ",f"nombre de rétablis : {model.recovered()}"]

    for i, text in enumerate(step_text):
        screen.blit(font.render(text, True, (255, 255, 255)), (10, 10 + i * 40))
    screen.blit(my_text, (225, 500))
    for agent in model.agents:
        if agent.status == "infecté":
            pygame.draw.circle(screen, (255, 0, 0), (agent.pos_x, agent.pos_y), 5)
        elif agent.status == "sain":
            pygame.draw.circle(screen, (0, 255, 0), (agent.pos_x, agent.pos_y), 5)
        else :
            pygame.draw.circle(screen, (0, 0, 255), (agent.pos_x, agent.pos_y), 5)

    pygame.display.flip()   
    clock.tick(60)          

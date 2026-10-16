import random

import mesa
from mesa import Agent
from mesa.datacollection import DataCollector

##Classe Agent
class HumanAgent(Agent):
    def __init__(self,model,height,width):
        super().__init__(model)
        self.pos_x = self.random.randint(100, 700)
        self.pos_y = self.random.randint(140, 500)
        self.vel_x = self.random.randint(-5, 5)
        self.vel_y = self.random.randint(-5, 5)

        self.days_lived = 0
        self.status= "sain"
        self.infected_days = 0
        self.height = height
        self.width = width
    
    def live_a_day(self):
        self.days_lived += 1
        if self.status == "infecté":
            self.infected_days += 1
            if self.infected_days >= 20:
                self.status = "rétabli"
                self.infected_days = 0
    def deplacement(self):
        if self.random.random() < 0.2:
            self.vel_x = self.random.randint(-5, 5)
            self.vel_y = self.random.randint(-5, 5)
        
        new_x = self.pos_x + self.vel_x
        new_y = self.pos_y + self.vel_y

        if new_x <= 0 or new_x >= self.model.width:
            self.vel_x = -self.vel_x

        if new_y <= 0 or new_y >= self.model.height:
            self.vel_y = -self.vel_y

        self.pos_x += self.vel_x
        self.pos_y += self.vel_y

##Classe modéle contenant les agents
class VirusSimulation(mesa.Model):
    def __init__(self,width, height, n,infected, rng= None):
        super().__init__(rng=rng)
        self.num_agents = n
        self.day = 0
        self.width = width
        self.height = height
        self.transmission_probability = 0.3

        HumanAgent.create_agents(model=self, n=n, height=height, width=width)
        infected_agents = self.random.sample(list(self.agents), infected)

        for agent in infected_agents:
            agent.status = "infecté"
        self.datacollector = DataCollector(
            model_reporters={
                "Jour": lambda m: m.day,
                "Nombre d'agents sains": lambda m: m.sain(),
                "Nombre d'agents infectés": lambda m: m.infected(),
                "Nombre d'agents rétablis": lambda m: m.recovered()
            }
            )
        self.datacollector.collect(self)
    def step(self):
        for agent in self.agents:
            agent.live_a_day()
            agent.deplacement()
        self.day += 1
        self.transmission()
        self.datacollector.collect(self)
    def transmission(self):
        infected_list= []
        sain_list = []
        for agent in self.agents:
            if agent.status == "infecté":
                infected_list.append(agent)
        for agent in self.agents:
            if agent.status == "sain":
                sain_list.append(agent)
        for agent in infected_list:
            for autre_agent in sain_list:
                    distance = ((agent.pos_x - autre_agent.pos_x) ** 2 + (agent.pos_y - autre_agent.pos_y) ** 2) ** 0.5
                    if distance < 50:
                        if self.random.random() < self.transmission_probability:
                            autre_agent.status = "infecté"
    def sain(self):
        return sum(1 for agent in self.agents if agent.status == "sain")
    def infected(self):
        return sum(1 for agent in self.agents if agent.status == "infecté")
    def recovered(self):
        return sum(1 for agent in self.agents if agent.status == "rétabli")
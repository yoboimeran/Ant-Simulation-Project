from food import Food, FoodMap
from parameters import *
import pygame
from vector import Vector
from math import ceil


def translateValue(value, min1, max1, min2, max2):
    return min2 + (max2 - min2) * ((value - min1) / (max1 - min1))


class Pheromone:
    def __init__(self, position, direction, type="Food"):
        self.position = position
        self.direction = direction
        self.strength = 100
        self.max_strength = 100
        self.evaporation_rate = evo_food_rate
        self.home_evaporation_rate = evo_home_rate
        self.color = green
        self.type = type
        self.radius = 2

    def Update(self):
        # reduce the pheromone
        if self.type == "food":
            self.strength -= self.evaporation_rate
        elif self.type == 'home':
            self.strength -= self.home_evaporation_rate

    def Show(self, screen, showFoodTrail, showHomeTrail):
        if showFoodTrail:
            if self.type == "food":
                val = max(self.strength, 1)
                alpha = int(translateValue(val, 0, 100, 1, 255))
                r, g, b = (red)
                surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA, 32)
                pygame.draw.circle(surface, (r, g, b, alpha), (self.radius, self.radius), self.radius)
                screen.blit(surface, (self.position - self.radius).xy())
        if showHomeTrail:
            if self.type == "home":
                val = max(self.strength, 1)
                alpha = int(translateValue(val, 0, 100, 1, 255))
                r, g, b = (13, 104, 222)
                surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA, 32)
                pygame.draw.circle(surface, (r, g, b, alpha), (self.radius, self.radius), self.radius)
                screen.blit(surface, (self.position - self.radius).xy())


class PheromoneMap:
    def __init__(self):
        self.home_pheromones = []
        self.food_pheromones = []
        self.pheromone_dispersion = pheromone_step
        self.radius = 2

    def ErasePheromone(self, screen, foods, showFoodTrail, showHomeTrail):
        # update pheromones and render
        # remove pheromone if it equal or inferior to zero
        for pher in self.food_pheromones:
            pher.Update()
            if pher.strength <= 0:
                self.food_pheromones.remove(pher)
                for food in foods:
                    if pher in food.pheromones:
                        food.pheromones.remove(pher)
            pher.Show(screen, showFoodTrail, showHomeTrail)
        for pher in self.home_pheromones:
            pher.Update()
            if pher.strength <= 0:
                self.home_pheromones.remove(pher)
            pher.Show(screen, showFoodTrail, showHomeTrail)

    def AppendPheromone(self, position, direction, pher_type="food", food=None):
        # Add pheromone based on it type(food or home)
        pher = Pheromone(position.Copy(), direction.Copy(), pher_type)
        selected_index = 0
        if pher_type.lower() == "food":
            selected_index = 0
        elif pher_type.lower() == "home":
            selected_index = 1

        if selected_index == 0:
            self.food_pheromones.append(pher)
            Food.AppendFoodPheromone(food, pher)
        elif selected_index == 1:
            self.home_pheromones.append(pher)

    def Update(self, screen, showFoodTrail, showHomeTrail, foods):
        self.ErasePheromone(screen, foods, showFoodTrail=showFoodTrail, showHomeTrail=showHomeTrail)



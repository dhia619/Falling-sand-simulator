import pygame

class Tool:
    def __init__(self,image_path,x,y):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=(x,y))
        self.hover_surface = pygame.Surface((self.image.get_width() + 10, self.image.get_height() + 10), pygame.SRCALPHA)
        self.hover_surface.fill((208,222,185,50))
    def draw(self,surface,mouse_pos):
        surface.blit(self.image,self.rect)
        if self.rect.collidepoint(mouse_pos):
            surface.blit(self.hover_surface,(self.rect.x -5 , self.rect.y -5))
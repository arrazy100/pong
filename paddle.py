import pygame

class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        # create paddle surface
        self.image = pygame.Surface([width, height])

        # fill paddle with black
        self.image.fill([0, 0, 0])

        # set colorkey to black
        self.image.set_colorkey([0, 0, 0])

        # draw rect
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        # get rect for collision detection
        self.rect = self.image.get_rect()

    # go up method
    def goUp(self, speed):
        self.rect.y -= speed

        # prevent paddle go out of window
        if self.rect.y < 55:
            self.rect.y = 55

    # go down method
    def goDown(self, speed):
        self.rect.y += speed

        # prevent paddle go out of window
        if self.rect.y > 384:
            self.rect.y = 384
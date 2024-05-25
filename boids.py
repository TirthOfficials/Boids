import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (25, 25, 45)
BOID_COLOR = (255, 200, 100)
NUM_BOIDS = 50
MAX_SPEED = 4
NEIGHBOR_RADIUS = 70
SEPARATION_RADIUS = 30
ALIGNMENT_RADIUS = 50
COHESION_RADIUS = 70
BOID_SIZE = 10
FONT_COLOR = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

def draw_text(text, position, font, color=FONT_COLOR):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, rect)

class Boid:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        angle = random.uniform(0, 2 * math.pi)
        self.velocity = pygame.Vector2(math.cos(angle), math.sin(angle)) * MAX_SPEED

    def update(self, boids):
        alignment = pygame.Vector2(0, 0)
        cohesion = pygame.Vector2(0, 0)
        separation = pygame.Vector2(0, 0)
        count = 0

        for boid in boids:
            distance = self.position.distance_to(boid.position)
            if boid != self and distance < NEIGHBOR_RADIUS:
                alignment += boid.velocity
                cohesion += boid.position
                if distance < SEPARATION_RADIUS:
                    separation += self.position - boid.position
                count += 1

        if count > 0:
            alignment /= count
            if alignment.length() > 0:
                alignment = (alignment.normalize() * MAX_SPEED) - self.velocity

            cohesion /= count
            if cohesion.length() > 0:
                cohesion = (cohesion - self.position).normalize() * MAX_SPEED

            if separation.length() > 0:
                separation = separation.normalize() * MAX_SPEED

            self.velocity += alignment + cohesion + separation
            if self.velocity.length() > 0:
                self.velocity = self.velocity.normalize() * MAX_SPEED

        self.position += self.velocity
        self.wrap_around()

    def wrap_around(self):
        if self.position.x > WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = WIDTH
        if self.position.y > HEIGHT:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = HEIGHT

    def draw(self, screen):
        angle = math.atan2(self.velocity.y, self.velocity.x)
        point_list = [
            (self.position.x + BOID_SIZE * math.cos(angle), self.position.y + BOID_SIZE * math.sin(angle)),
            (self.position.x + BOID_SIZE * math.cos(angle + 2.5), self.position.y + BOID_SIZE * math.sin(angle + 2.5)),
            (self.position.x + BOID_SIZE * math.cos(angle - 2.5), self.position.y + BOID_SIZE * math.sin(angle - 2.5))
        ]
        pygame.draw.polygon(screen, BOID_COLOR, point_list)

def main_menu():
    in_menu = True
    start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 20, 200, 40)
    exit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 40)

    while in_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    in_menu = False
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        screen.fill(BACKGROUND_COLOR)
        draw_text("Boids Simulation", (WIDTH // 2, HEIGHT // 4), font, FONT_COLOR)
        pygame.draw.rect(screen, (0, 255, 0), start_button)
        draw_text("Start New Game", start_button.center, font)
        pygame.draw.rect(screen, (255, 0, 0), exit_button)
        draw_text("Exit", exit_button.center, font)
        pygame.display.flip()
        clock.tick(15)

# Create boids
boids = [Boid(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(NUM_BOIDS)]

# Start menu
main_menu()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BACKGROUND_COLOR)

    # Drawing a subtle gradient in the background for visual interest
    for y in range(HEIGHT):
        gradient_color = (BACKGROUND_COLOR[0], BACKGROUND_COLOR[1], BACKGROUND_COLOR[2] + y // 10 % 30)
        pygame.draw.line(screen, gradient_color, (0, y), (WIDTH, y))

    for boid in boids:
        boid.update(boids)
        boid.draw(screen)

    # Display the count of the largest flock
    draw_text(f"Largest Flock: {len(boids)}", (WIDTH - 120, 20), font)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

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
OBSTACLE_COLOR = (200, 50, 50)
MAX_SPEED = 4
NEIGHBOR_RADIUS = 70
SEPARATION_RADIUS = 30
ALIGNMENT_RADIUS = 50
COHESION_RADIUS = 70
BOID_SIZE = 10
FONT_COLOR = (255, 255, 255)
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 250  # Radius of the circle in which the boids are confined

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
boids = []
obstacles = []

def draw_text(text, position, font, color=FONT_COLOR):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, rect)

class Boid:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        angle = random.uniform(0, 2 * math.pi)
        self.velocity = pygame.Vector2(math.cos(angle), math.sin(angle)) * MAX_SPEED

    def update(self, boids, obstacles):
        alignment = pygame.Vector2(0, 0)
        cohesion = pygame.Vector2(0, 0)
        separation = pygame.Vector2(0, 0)
        count = 0

        for other in boids:
            if other is not self:
                distance = self.position.distance_to(other.position)
                if distance < NEIGHBOR_RADIUS:
                    alignment += other.velocity
                    cohesion += other.position
                    if distance < SEPARATION_RADIUS:
                        separation += (self.position - other.position) / distance
                    count += 1

        for obstacle in obstacles:
            dist_to_obstacle = self.position.distance_to(obstacle)
            if dist_to_obstacle < NEIGHBOR_RADIUS:
                separation += (self.position - obstacle) * 5 / dist_to_obstacle

        if count > 0:
            alignment /= count
            cohesion /= count
            target_direction = (cohesion - self.position) / 100
            self.velocity += (alignment + target_direction + separation)
            if self.velocity.length() > 0:
                self.velocity = self.velocity.normalize() * MAX_SPEED

        self.position += self.velocity
        self.stay_within_circle()

    def stay_within_circle(self):
        if self.position.distance_to(pygame.Vector2(CENTER)) > RADIUS:
            direction_to_center = (pygame.Vector2(CENTER) - self.position).normalize()
            self.velocity = direction_to_center * MAX_SPEED

    def draw(self, screen):
        angle = math.atan2(self.velocity.y, self.velocity.x)
        points = [
            (self.position.x + BOID_SIZE * math.cos(angle), self.position.y + BOID_SIZE * math.sin(angle)),
            (self.position.x + BOID_SIZE * math.cos(angle + 2.5), self.position.y + BOID_SIZE * math.sin(angle + 2.5)),
            (self.position.x + BOID_SIZE * math.cos(angle - 2.5), self.position.y + BOID_SIZE * math.sin(angle - 2.5))
        ]
        pygame.draw.polygon(screen, BOID_COLOR, points)

def is_within_circle(point):
    return math.sqrt((point[0] - CENTER[0])**2 + (point[1] - CENTER[1])**2) <= RADIUS

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

# Start menu
main_menu()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                # Add a new boid at a random position within the circle
                angle = random.uniform(0, 2 * math.pi)
                radius = random.uniform(0, RADIUS)
                x = CENTER[0] + radius * math.cos(angle)
                y = CENTER[1] + radius * math.sin(angle)
                boids.append(Boid(x, y))
            elif event.key == pygame.K_h:
                # Add a new obstacle at a random position within the circle
                angle = random.uniform(0, 2 * math.pi)
                radius = random.uniform(0, RADIUS)
                x = CENTER[0] + radius * math.cos(angle)
                y = CENTER[1] + radius * math.sin(angle)
                obstacles.append(pygame.Vector2(x, y))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if is_within_circle(mouse_pos):
                obstacles.append(pygame.Vector2(mouse_pos[0], mouse_pos[1]))

    screen.fill(BACKGROUND_COLOR)

    # Draw the circle boundary
    pygame.draw.circle(screen, FONT_COLOR, CENTER, RADIUS, 1)

    for obstacle in obstacles:
        pygame.draw.circle(screen, OBSTACLE_COLOR, (int(obstacle.x), int(obstacle.y)), 10)

    for boid in boids:
        boid.update(boids, obstacles)
        boid.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

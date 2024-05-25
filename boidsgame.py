import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (10, 10, 40)
OBSTACLE_COLOR = (200, 50, 50)
TEXT_COLOR = (0, 0, 0)  # Black color for text
NEIGHBOR_RADIUS = 45
SEPARATION_RADIUS = 30
ALIGNMENT_RADIUS = 50
COHESION_RADIUS = 70
BOID_SIZE = 20
FONT_COLOR = (255, 255, 255)
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 250  # Radius of the circle in which the boids are confined
MAX_SPEED = 4  # Initial maximum speed of boids
CIRCLE_COLOR = (0, 0, 139)  # Dark blue color for circle
CIRCLE_BORDER_WIDTH = 5  # Thickness of the circle border

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)
bold_font = pygame.font.Font(None, 24)  # Bold font for text
boids = []
obstacles = []

background_image = pygame.image.load(r'bg.jpeg')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
boid_image = pygame.image.load(r'bird.png')
boid_image = pygame.transform.scale(boid_image, (BOID_SIZE, BOID_SIZE))

def draw_text(text, position, font, color=TEXT_COLOR, center=True):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    if center:
        rect.center = position
    else:
        rect.topleft = position
    screen.blit(text_surface, rect)

def draw_background():
    screen.blit(background_image, (0, 0))

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
            if dist_to_obstacle < 50:
                if dist_to_obstacle == 0:
                    dist_to_obstacle = 0.1  # Prevent division by zero
                separation += (self.position - obstacle) * (50 / dist_to_obstacle)**2

        if count > 0:
            alignment /= count
            cohesion /= count
            cohesion_direction = (cohesion - self.position) / 100
            self.velocity += (alignment + cohesion_direction + separation)
            if self.velocity.length() > 0:
                self.velocity = self.velocity.normalize() * MAX_SPEED

        self.position += self.velocity
        self.stay_within_circle()

    def stay_within_circle(self):
        if self.position.distance_to(pygame.Vector2(CENTER)) > RADIUS:
            direction_to_center = (pygame.Vector2(CENTER) - self.position).normalize()
            self.velocity = direction_to_center * MAX_SPEED

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(boid_image, -self.velocity.angle_to(pygame.Vector2(1, 0)))
        screen.blit(rotated_image, self.position - (BOID_SIZE / 2, BOID_SIZE / 2))

def is_within_circle(point):
    return math.sqrt((point[0] - CENTER[0])**2 + (point[1] - CENTER[1])**2) <= RADIUS

def draw_slider(value):
    pygame.draw.rect(screen, TEXT_COLOR, (20, 20, 150, 10))
    pygame.draw.circle(screen, TEXT_COLOR, (20 + int(value * 150), 25), 10)

def main_menu():
    running = True
    while running:
        draw_background()
        draw_text("Press any key to start the simulation.", (WIDTH // 2, HEIGHT // 2), font)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                running = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

main_menu()

# Game loop
running = True
speed_factor = 0.5  # Initial speed factor
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
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
                if is_within_circle((x, y)):
                    obstacles.append(pygame.Vector2(x, y))
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if is_within_circle(mouse_pos):
                obstacles.append(pygame.Vector2(mouse_pos[0], mouse_pos[1]))
        elif event.type == pygame.MOUSEMOTION:
            if 10 <= event.pos[0] <= 170 and 15 <= event.pos[1] <= 35:
                speed_factor = (event.pos[0] - 20) / 150
                MAX_SPEED = 1 + speed_factor * 9

    draw_background()
    pygame.draw.circle(screen, CIRCLE_COLOR, CENTER, RADIUS, CIRCLE_BORDER_WIDTH)  # Draw boundary

    for obstacle in obstacles:
        pygame.draw.circle(screen, OBSTACLE_COLOR, (int(obstacle.x), int(obstacle.y)), 10)

    for boid in boids:
        boid.update(boids, obstacles)
        boid.draw(screen)

    # Display instructions and stats
    draw_text("Press 'B' to add new boid", (10, 60), bold_font, TEXT_COLOR, center=False)
    draw_text("Press 'H'/ click to add obstacle", (10, 90), bold_font, TEXT_COLOR, center=False)
    draw_text("Press 'Q' to end the Game", (10, 120), bold_font, TEXT_COLOR, center=False)
    draw_text(f"Total Boids: {len(boids)}", (10, 150), bold_font, TEXT_COLOR, center=False)
    draw_text(f"Total Obstacles: {len(obstacles)}", (10, 180), bold_font, TEXT_COLOR, center=False)

    # Draw speed slider
    draw_text("Speed", (10, 0), bold_font, TEXT_COLOR, center=False)
    draw_slider(speed_factor)

    pygame.display.flip()
    clock.tick(60)

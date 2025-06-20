import pygame
import random
import math
import time
import matplotlib.pyplot as plt
import imageio
import numpy as np

# Constants
WIDTH, HEIGHT = 800, 600
HOME_ZONE = (WIDTH // 2, HEIGHT // 2)
OBJECT_RADIUS = 5
ROBOT_RADIUS = 10
NUM_OBJECTS = 30
PROXIMITY_RANGE = 40
SIM_DURATION = 30
SIM_STEPS = 1800

BLACK = (0, 0, 0)
LIGHT_ZONE_COLOR = (255, 255, 100)
OBJECT_COLOR = (200, 0, 0)
ROBOT_COLOR = (0, 200, 255)
PUSHING_COLOR = (255, 150, 0)

pygame.init()
font = pygame.font.SysFont(None, 24)

class Object:
    def __init__(self, x, y):
        self.pos = [x, y]
        self.carried = False
        self.delivered = False

class Robot:
    def __init__(self):
        self.pos = [random.randint(0, WIDTH), random.randint(0, HEIGHT)]
        self.carrying = False
        self.target = None
        self.speed = 1.5
        self.pushing_obj = None

    def avoid_robots(self, robots):
        repulsion_x = 0
        repulsion_y = 0
        for other in robots:
            if other is not self:
                dx = other.pos[0] - self.pos[0]
                dy = other.pos[1] - self.pos[1]
                dist = math.hypot(dx, dy)
                if dist < PROXIMITY_RANGE and dist > 0:
                    strength = (PROXIMITY_RANGE - dist) / PROXIMITY_RANGE
                    repulsion_x -= dx / dist * strength
                    repulsion_y -= dy / dist * strength

        self.pos[0] += repulsion_x * 10
        self.pos[1] += repulsion_y * 10
        self.pos[0] = max(ROBOT_RADIUS, min(WIDTH - ROBOT_RADIUS, self.pos[0]))
        self.pos[1] = max(ROBOT_RADIUS, min(HEIGHT - ROBOT_RADIUS, self.pos[1]))

    def move_toward(self, target_pos):
        dx, dy = target_pos[0] - self.pos[0], target_pos[1] - self.pos[1]
        dist = math.hypot(dx, dy)
        if dist > 0:
            dx /= dist
            dy /= dist
            self.pos[0] += dx * self.speed
            self.pos[1] += dy * self.speed
        return dx, dy

    def update(self, objects, robots):
        self.avoid_robots(robots)
        if self.carrying and self.pushing_obj:
            dx, dy = self.move_toward(HOME_ZONE)
            offset = ROBOT_RADIUS + OBJECT_RADIUS + 2
            self.pushing_obj.pos[0] = self.pos[0] + dx * offset
            self.pushing_obj.pos[1] = self.pos[1] + dy * offset

            if math.hypot(self.pos[0] - HOME_ZONE[0], self.pos[1] - HOME_ZONE[1]) < 30:
                self.carrying = False
                self.pushing_obj.delivered = True
                self.pushing_obj.carried = False
                self.pushing_obj = None
                self.target = None
        else:
            nearest_obj = None
            min_dist = float('inf')
            for obj in objects:
                if not obj.carried and not obj.delivered:
                    dist = math.hypot(self.pos[0] - obj.pos[0], self.pos[1] - obj.pos[1])
                    if dist < min_dist:
                        min_dist = dist
                        nearest_obj = obj
            if nearest_obj:
                self.target = nearest_obj
                self.move_toward(nearest_obj.pos)
                if min_dist < ROBOT_RADIUS + OBJECT_RADIUS:
                    self.carrying = True
                    nearest_obj.carried = True
                    self.pushing_obj = nearest_obj

def run_simulation(swarm_size, draw=False, record_video=False):
    if draw:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(f"Foraging Simulation - Swarm Size: {swarm_size}")
        clock = pygame.time.Clock()
    else:
        screen = None

    robots = [Robot() for _ in range(swarm_size)]
    objects = [Object(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)) for _ in range(NUM_OBJECTS)]

    frames = []
    steps = 0
    start_time = time.time()

    while True:
        if draw:
            screen.fill(BLACK)
            pygame.draw.circle(screen, LIGHT_ZONE_COLOR, HOME_ZONE, 30)
            home_text = font.render("HOME", True, BLACK)
            screen.blit(home_text, (HOME_ZONE[0] - 20, HOME_ZONE[1] - 10))

        for event in pygame.event.get() if draw else []:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        for obj in objects:
            if draw and not obj.delivered:
                pygame.draw.circle(screen, OBJECT_COLOR, (int(obj.pos[0]), int(obj.pos[1])), OBJECT_RADIUS)

        for robot in robots:
            robot.update(objects, robots)
            color = PUSHING_COLOR if robot.carrying else ROBOT_COLOR
            if draw:
                pygame.draw.circle(screen, color, (int(robot.pos[0]), int(robot.pos[1])), ROBOT_RADIUS)

        if draw:
            pygame.display.flip()
            if record_video:
                frame = pygame.surfarray.array3d(pygame.display.get_surface())
                frame = np.transpose(frame, (1, 0, 2))  # convert to (height, width, color)
                frames.append(frame)
            clock.tick(60)
            if time.time() - start_time >= SIM_DURATION:
                break
        else:
            steps += 1
            if steps >= SIM_STEPS:
                break

    if record_video:
        imageio.mimsave("simulation_swarm5.mp4", frames, fps=60)
        print("🎥 Video saved as simulation_swarm5.mp4")

    return sum(1 for obj in objects if obj.delivered)

# Run simulations
swarm_sizes = [1, 3, 5, 7, 10]
results = []

print("🚀 Running simulations...")
for size in swarm_sizes:
    print(f"Swarm Size: {size}")
    collected = run_simulation(size, draw=(size == 5), record_video=(size == 5))
    print(f"  Collected: {collected} objects")
    results.append(collected)

# Plot and save graph
plt.figure(figsize=(8, 6))
plt.plot(swarm_sizes, results, marker='o', color='green')
plt.title("Objects Collected vs Swarm Size (30s)")
plt.xlabel("Swarm Size")
plt.ylabel("Objects Collected")
plt.grid(True)
plt.savefig("collected_vs_swarm_size.png")
print("📈 Graph saved as collected_vs_swarm_size.png")
plt.show()

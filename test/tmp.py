import pygame
import sys

# === 座標読み込み ===
def load_xyz_frames(path, n_particles):
    frames = []
    with open(path, "r") as f:
        for line in f:
            parts = list(map(float, line.split()))
            frame = []
            for i in range(n_particles):
                x = parts[i*3 + 0]
                y = parts[i*3 + 1]
                z = parts[i*3 + 2]
                frame.append((x, y, z))
            frames.append(frame)
    return frames

# === pygame 初期化 ===
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("XYZ Animation")
clock = pygame.time.Clock()

# === 設定 ===
n_particles = 5
frames = load_xyz_frames("./test/tmp.txt", n_particles)
frame_index = 0
scale = 100
offset_x, offset_y = WIDTH//2, HEIGHT//2

# === メインループ ===
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))

    # 現在フレームの全粒子を描画
    for x, y, z in frames[frame_index]:
        sx = int(x * scale + offset_x)
        sy = int(y * scale + offset_y)
        pygame.draw.circle(screen, (255, 255, 255), (sx, sy), 5)

    pygame.display.flip()

    frame_index = (frame_index + 1) % len(frames)
    clock.tick(60)

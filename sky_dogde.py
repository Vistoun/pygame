import pygame
import random


from pygame.locals import(
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Text(pygame.sprite.Sprite):
    def __init__(self, text, size, color):
        super(Text, self).__init__()
        self.font = pygame.font.SysFont("Arial", size)
        self.color = color
        self.surf = self.font.render(text, 1, self.color)
        self.rect = self.surf.get_rect()

    def update(self, text):
        self.surf = self.font.render(text, 1, (self.color))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("images/jet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -1)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 1)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-1, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(1, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("images/missile.png")
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(1, 2)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("images/cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, center, direction=0, speed=2):
        super(Bullet, self).__init__()
        self.surf = pygame.Surface((15, 10))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center=center)
        self.direction = direction
        self.speed = speed

    def update(self):
        self.rect.move_ip(self.speed, self.direction)
        if self.rect.left > SCREEN_WIDTH:
            self.kill()


class Power_up(pygame.sprite.Sprite):
    def __init__(self):
        super(Power_up, self).__init__()
        self.surf = pygame.Surface((10, 15))
        self.surf.fill((0, 255, 0))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()


pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)
ADDPOWER_UP = pygame.USEREVENT + 3
pygame.time.set_timer(ADDPOWER_UP, 800)

player = Player()
power_text = Text("Power", 20, "black")
enemies_killed_text = Text("Score", 20, "black")

enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
bullets = pygame.sprite.Group()
power_bullets_up = pygame.sprite.Group()
power_bullets_down = pygame.sprite.Group()
power_ups = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(power_text)
all_sprites.add(enemies_killed_text)


enemies_killed_text.rect.x = SCREEN_WIDTH - 80
enemies_killed_text.rect.y = 0
power_text.rect.x = SCREEN_WIDTH - 80
power_text.rect.y = 20

power_bullets_up_state = False
power_bullets_down_state = False
power = 2
power_display = 0
enemies_killed = 0
running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                new_bullet = Bullet(player.rect.center, 0, power)
                bullets.add(new_bullet)
                all_sprites.add(new_bullet)

                if power_bullets_up_state:
                    new_power_bullet_up = Bullet(player.rect.center, -2, power)
                    bullets.add(new_power_bullet_up)
                    all_sprites.add(new_power_bullet_up)

                if power_bullets_down_state:
                    new_power_bullet_down = Bullet(player.rect.center, 2, power)
                    bullets.add(new_power_bullet_down)
                    all_sprites.add(new_power_bullet_down)

            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

        elif event.type == ADDPOWER_UP:
            new_power_up = Power_up()
            power_ups.add(new_power_up)
            all_sprites.add(new_power_up)

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()
    clouds.update()
    bullets.update()
    power_ups.update()
    enemies_killed_text.update(f"Score {enemies_killed}")
    power_text.update(f"Power: {power_display}")

    screen.fill((135, 206, 250))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    for enemy in enemies:
        if pygame.sprite.spritecollide(enemy, bullets, dokill=True):
            enemies_killed += 1
            enemy.kill()

    for power_up in power_ups:
        if pygame.sprite.spritecollideany(player, power_ups):
            if(power != 12):
                power += 1
                power_display += 1

            if power == 6:
                power_bullets_down_state = True
            if power == 10:
                power_bullets_up_state = True

            power_up.kill()

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False

    pygame.display.flip()

    clock.tick(144)
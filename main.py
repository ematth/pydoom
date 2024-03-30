import pygame as pg
import numpy as np

def main():
    pg.init()
    display: tuple[int] = (1280, 720)
    screen: pg.Display = pg.display.set_mode(display)
    running: bool = True
    clock = pg.time.Clock()

    HRES: int = 120 # horizontal resolution
    HALFVRES: int = 100 # vertical resolution / 2

    mod: float = HRES / 60
    pos_x, pos_y, rot = 0, 0, 0
    frame = np.random.uniform(0, 1, (HRES, HALFVRES * 2, 3))

    while running:
        for event in pg.event.get():
            if event.type is pg.QUIT:
                running = False
        
        for i in range(HRES):
            rot_i = rot + np.deg2rad(i/mod - 30)
            sin, cos = np.sin(rot_i), np.cos(rot_i)

            for j in range(HALFVRES):
                n = HALFVRES / (HALFVRES - j)
                x, y = pos_x + cos*n, pos_y + sin*n

                frame[i][HALFVRES * 2 - j - 1] = [0, 0, 0] if int(x)%2 == int(y)%2 else [1, 1, 1]

        surf = pg.surfarray.make_surface(frame * 255)
        surf = pg.transform.scale(surf, display)

        screen.blit(surf, (0, 0))
        pg.display.update()

        pos_x, pos_y, rot = movement(pos_x, pos_y, rot, pg.key.get_pressed())


def movement(pos_x, pos_y, rot, keys, c=1, d=1):
    if keys[pg.K_LEFT]:
        rot = rot - (0.1 * c)

    if keys[pg.K_RIGHT]:
        rot = rot + (0.1 * c)

    if keys[pg.K_UP]:
        pos_x, pos_y = pos_x + np.cos(rot)*0.1*d, pos_y + np.sin(rot)*0.1*d

    if keys[pg.K_DOWN]:
        pos_x, pos_y = pos_x - np.cos(rot)*0.1*d, pos_y - np.sin(rot)*0.1*d  

    return pos_x, pos_y, rot


if __name__ == '__main__':
    main()
    pg.quit()
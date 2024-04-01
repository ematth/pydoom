import pygame as pg
import numpy as np
from numba import njit

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
    frame = np.full((HRES, HALFVRES * 2, 3), 0.5)
    sky = pg.image.load('skybox2.jpg')
    sky = pg.surfarray.array3d(pg.transform.scale(sky, (360, HALFVRES*2)))/255
    floor = pg.surfarray.array3d(pg.image.load('floor.jpg'))/255

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        frame = new_frame(pos_x, pos_y, rot, frame, sky, floor, HRES, HALFVRES, mod)
        

        surf = pg.surfarray.make_surface(frame * 255)
        surf = pg.transform.scale(surf, display)

        screen.blit(surf, (0, 0))
        pg.display.update()

        pos_x, pos_y, rot = movement(pos_x, pos_y, rot, pg.key.get_pressed(), clock.tick())

@njit
def new_frame(posx, posy, rot, frame, sky, floor, hres, halfvres, mod):
    for i in range(hres):
        rot_i = rot + np.deg2rad(i/mod - 30)
        sin, cos, cos2 = np.sin(rot_i), np.cos(rot_i), np.cos(np.deg2rad(i/mod - 30))
        frame[i][:] = sky[int(np.rad2deg(rot_i)%359)][:]
        for j in range(halfvres):
            n = (halfvres/(halfvres-j))/cos2
            x, y = posx + cos*n, posy + sin*n
            xx, yy = int(x*2%1*99), int(y*2%1*99)

            shade = 0.2 + 0.8*(1-j/halfvres)

            frame[i][halfvres*2-j-1] = shade*floor[xx][yy]

    return frame


def movement(pos_x, pos_y, rot, keys, et):
    if keys[pg.K_LEFT]:
        rot -= 0.001*et

    if keys[pg.K_RIGHT]:
        rot += 0.001*et

    if keys[pg.K_UP]:
        pos_x, pos_y = pos_x + np.cos(rot)*0.002*et, pos_y + np.sin(rot)*0.002*et

    if keys[pg.K_DOWN]:
        pos_x, pos_y = pos_x - np.cos(rot)*0.002*et, pos_y - np.sin(rot)*0.002*et

    return pos_x, pos_y, rot


if __name__ == '__main__':
    main()
    pg.quit()
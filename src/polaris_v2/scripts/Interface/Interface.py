#!/usr/bin/env python3

import rospy
import pygame

def interface(V, W, distance):

    pygame.init()  # Pygame'i başlat
    imp = pygame.image.load("interface_example.jpg")
    size= imp.get_size()
    display_surface = pygame.display.set_mode(size, pygame.RESIZABLE)
    pygame.display.set_caption("Komut Arayüzü")
    font = pygame.font.SysFont('freesanbold.ttf', 14)

    running = True
    fullscreen = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    if not fullscreen:
                        display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        fullscreen = True
                    else:
                        display_surface = pygame.display.set_mode((600, 338), pygame.RESIZABLE)
                        fullscreen = False
            elif event.type == pygame.VIDEORESIZE:
                display_surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        display_surface.fill((255, 255, 255))

        # Ekranın boyutlarını alın
        screen_width, screen_height = display_surface.get_size()

        # Resmi ve metni ekran boyutuna göre yeniden konumlandırın
        imp_scaled = pygame.transform.scale(imp, (screen_width, screen_height))
        display_surface.blit(imp_scaled, (0, 0))

        # Odometry bilgilerini göster
        if V and W and distance:
            text = font.render("Görev Başladı...", True, (0, 0, 0))
            velocity_text = font.render(
                f"Hız(m/s): {V:.2f}", True, (0, 0, 0))
            angular_text = font.render(
                f"Açısal Hız(rad/s): {W:.2f}", True, (0, 0, 0))
            position_text = font.render(
                f"Distance(m): {distance:.2f}", True, (0, 0, 0))


            display_surface.blit(text, (int(screen_width * 0.62), int(screen_height * 0.41)))
            display_surface.blit(velocity_text, (int(screen_width * 0.62), int(screen_height * 0.50)))
            display_surface.blit(angular_text, (int(screen_width * 0.62), int(screen_height * 0.59)))
            display_surface.blit(position_text, (int(screen_width * 0.62), int(screen_height * 0.68)))


        # Ekranı güncelleyin
        pygame.display.flip()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            W = 0.5  # Rotate with angular velocity of 0.1 rad/s
        elif keys[pygame.K_RIGHT]:
            W = -0.5  # Rotate with angular velocity of -0.1 rad/s
        else:
           W = 0  # Rotate with angular velocity of 0.1 rad/s

        if keys[pygame.K_UP]:
            V = 1  # Move forward with linear velocity of 0.5 m/s
            if keys[pygame.K_SPACE]:
                V += 0.1
            else:
                V = 0.5

        elif keys[pygame.K_DOWN]:
            V = -0.5  # Move back with linear velocity of 0.5 m/s
            if keys[pygame.K_SPACE]:
                V -= 0.1
            else:
                V = -0.5
        else:
            v = 0  # Move back with linear velocity of 0.5 m/s



if __name__ == '__main__':
    try:
        move_robot()
    except rospy.ROSInterruptException:
        pass

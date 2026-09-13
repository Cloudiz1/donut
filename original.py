import math
import os

# how much to increment our rotations by
theta_spacing = 0.07;
phi_spacing = 0.02

R1 = 1
R2 = 2
K2 = 8

screen_width = os.get_terminal_size(0).columns
screen_height = os.get_terminal_size(0).lines
aspect_ratio = screen_width / screen_height

K1x = screen_width / (R1 + R2)
K1y = K1x / aspect_ratio * 1.5

def render_frame(A, B):
    cosA = math.cos(A)
    sinA = math.sin(A)
    cosB = math.cos(B)
    sinB = math.sin(B)

    output = [[' ' for _ in range(screen_width)] for _ in range(screen_height)]
    zbuffer = [[0 for _ in range(screen_width)] for _ in range(screen_height)]

    theta = 0
    while theta < 2 * math.pi:
        costheta = math.cos(theta)
        sintheta = math.sin(theta)

        phi = 0
        while phi < 2 * math.pi:
            cosphi = math.cos(phi)
            sinphi = math.sin(phi)

            circlex = R2 + R1*costheta
            circley = R1*sintheta

            x = circlex*(cosB*cosphi + sinA*sinB*sinphi) - circley*cosA*sinB
            y = circlex*(sinB*cosphi - sinA*cosB*sinphi) + circley*cosA*cosB
            z = K2 + cosA*circlex*sinphi + circley*sinA

            xp = math.floor(screen_width / 2 + K1x*x/z)
            yp = math.floor(screen_height / 2 - K1y*y/z)

            L = cosphi*costheta*sinB - cosA*costheta*sinphi - sinA*sintheta + cosB*(cosA*sintheta - costheta*sinA*sinphi)
            if L > 0 and 1/z > zbuffer[yp][xp]:
                zbuffer[yp][xp] = 1/z
                luminance_index = math.floor(L*8)
                output[yp][xp] = ".,-~:;=!*#$@"[luminance_index]

            phi += phi_spacing

        theta += theta_spacing

    print("\033[2J\033[H", end="")
    for row in output:
        for char in row:
            print(char, end="")

        print()

A, B = 0, 0
while True:
    A += theta_spacing
    B += phi_spacing 
    render_frame(A, B)

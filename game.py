# Projection of 3D objects onto 2D screen in games
# Author Tushar Mahat, Nabin Bhandari

import pygame
import numpy as np
from math import *
import sys

# Initialize pygame and create window
pygame.init()

pygame.font.init() # you have to call this at the start, 
pygame.display.set_caption("3D Vizualization in 2D plane")

my_font = pygame.font.SysFont('Arial', 12)
btn_font = pygame.font.SysFont('Arial', 18)
angleX=0
angleY=0
angleZ=0
width, height = 800, 750
OFFSET_X=width/2
OFFSET_Y=height/2
screen = pygame.display.set_mode((width, height))
scaler=100
DOT_RADIUS=5
perspectiveOn=False

# white color
color = (255,255,255)

# light shade of the button
color_light = (170,170,170)

# dark shade of the button
color_dark = (100,100,100)

COLORS=[(255,255,255),(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255),(0,128,0)]

VERTICES=[]
VERTICES.append(np.matrix([[1,1,1]]))
VERTICES.append(np.matrix([1,-1,1]))
VERTICES.append(np.matrix([1,-1,-1]))
VERTICES.append(np.matrix([1,1,-1]))
VERTICES.append(np.matrix([-1,1,1]))
VERTICES.append(np.matrix([-1,-1,1]))
VERTICES.append(np.matrix([-1,-1,-1]))
VERTICES.append(np.matrix([-1,1,-1]))

# create point at origin
ORIGIN=pygame.Rect(OFFSET_X-2, OFFSET_Y-2, DOT_RADIUS, DOT_RADIUS)

# ----------------------------------------------------------------------
projection_matrix_3by3=np.matrix([
    [1,0,0],
    [0,1,0],
    [0,0,0]])

def showText(text,co_ordinates,color):
    text_surface = my_font.render(text, True, color)
    screen.blit(text_surface, co_ordinates)


def printProjectedPoints():
    for point in VERTICES:
        projected2d=np.dot(projection_matrix_3by3,point.reshape((3,1)))
        print(projected2d)
printProjectedPoints()

projected_points=[[n,n]for n in range(len(VERTICES))]

def connectPoints(i,j,points):
    pygame.draw.line(screen,(255,255,255),(points[i][0],points[i][1]),(points[j][0],points[j][1]))

def createBtn(str,x,y,w,h):
    pygame.draw.rect(screen,color_dark,[x,y,w,h])
    # superimposing the text onto our button
    text = btn_font.render(str , True , color)
    screen.blit(text , (x+15,y+10))

# Game loop----------------------------------------------------------------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #checks if a mouse is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:

            #if the mouse is clicked on the
            # button the game is terminated
            if width-100 <= mouse[0] <= width-100+70 and height-60 <= mouse[1] <= height-60+40:
                pygame.quit()
            if width-100 <= mouse[0] <= width-100+70 and height-120 <= mouse[1] <= height-120+40:
                angleX=angleY=angleZ=0
                projection_matrix_3by3=np.matrix([
                [1,0,0],
                [0,1,0],
                [0,0,0]])
            if width-300 <= mouse[0] <= width-300+150 and height-60 <= mouse[1] <= height-60+40:
                angleX+=0.02
            if width-700 <= mouse[0] <= width-700+60 and height-60 <= mouse[1] <= height-60+40:
                angleX-=0.02
            if width-300 <= mouse[0] <= width-300+60 and height-120 <= mouse[1] <= height-120+40:
                angleY+=0.02
            if width-700 <= mouse[0] <= width-700+60 and height-120 <= mouse[1] <= height-120+40:
                angleY-=0.02
            if width-300 <= mouse[0] <= width-300+60 and height-180 <= mouse[1] <= height-180+40:
                angleZ+=0.02
            if width-700 <= mouse[0] <= width-700+60 and height-180 <= mouse[1] <= height-180+40:
                angleZ-=0.02
            if width-120 <= mouse[0] <= width-120+120 and height-180 <= mouse[1] <= height-180+40:
                perspectiveOn=not perspectiveOn
                projection_matrix_3by3=np.matrix([
                [1,0,0],
                [0,1,0],
                [0,0,0]])

    mouse = pygame.mouse.get_pos()    

    # Clear screen
    screen.fill((0, 0, 0))
    pygame.draw.line(screen,(20,255,20),(width/2,0),(width/2,height))
    showText('+Y',(width/2,0),(255,255,255))
    showText('-Y',(width/2,height-15),(255,255,255))

    pygame.draw.line(screen,(255,20,20),(0,height/2),(width,height/2))
    showText('-X',(0,height/2),(255,255,255))
    showText('+X',(width-15,height/2),(255,255,255))

    showText('(0,0)',(OFFSET_X-8, OFFSET_Y+10),(70,130,180))

    createBtn('Quit',width-100,height-60,70,40)
    createBtn('Reset',width-100,height-120,70,40)
    createBtn('Perspective',width-120,height-180,120,40)
    createBtn('<-x',width-300,height-60,60,40)
    createBtn('x->',width-700,height-60,60,40)
    createBtn('<-y',width-300,height-120,60,40)
    createBtn('y->',width-700,height-120,60,40)
    createBtn('<-z',width-300,height-180,60,40)
    createBtn('z->',width-700,height-180,60,40)

    # draw ORIGIN
    pygame.draw.ellipse(screen, (255,255,255), ORIGIN)
    showText('(0,0)',(OFFSET_X-8, OFFSET_Y+10),(70,130,180))

    # 
    rotation_x=np.matrix([
        [1,0,0],
        [0,cos(angleX),-sin(angleX)],
        [0,sin(angleX),cos(angleX)]
    ])

    rotation_y=np.matrix([
        [cos(angleY),0,sin(angleY)],
        [0,1,0],
        [-sin(angleY),0,cos(angleY)]
    ])
    
    rotation_z=np.matrix([
        [cos(angleZ),-sin(angleZ),0],
        [sin(angleZ),cos(angleZ),0],
        [0,0,1]
    ])

    # Draw 8 co-ordinates for cube
    for index,point in enumerate(VERTICES):
        rotated_along_z=np.dot(rotation_z,point.reshape((3,1)))
        rotated_along_y=np.dot(rotation_y,rotated_along_z)
        rotated_along_x=np.dot(rotation_x,rotated_along_y)

        if(perspectiveOn):
            distance=1.7
            z=1/(distance-rotated_along_x[2,0])
            projection_matrix_3by3=np.matrix([
                [z,0,0],
                [0,z,0],
                [0,0,0]])

        projected2d=np.dot(projection_matrix_3by3,rotated_along_x)
        # projected2d=np.dot(projection_matrix_3by3,point.reshape((3,1)))
        x=int(projected2d[0][0]*scaler)+OFFSET_X
        y=int(projected2d[1][0]*scaler)+OFFSET_Y

        showText('('+str(x-OFFSET_X)+','+str(-y+OFFSET_Y)+')',(x-5,y+5),COLORS[index])
        pygame.draw.circle(screen,COLORS[index],(x,-y),DOT_RADIUS)

        projected_points[index]=[x,y]

        pygame.draw.circle(screen,COLORS[index],(x,y),DOT_RADIUS)

    for p in range(4):
        connectPoints(p,(p+1)%4,projected_points)
        connectPoints(p+4,(p+1)%4+4,projected_points)
        connectPoints(p,p+4,projected_points)
    # Update display
    pygame.display.flip()

    # Delay to control frame rate
    pygame.time.wait(60)
    

# Clean up and exit
pygame.quit()
import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image
import random
import math
snowmanPosition = [0, 0, 0]

CameraPos = [snowmanPosition[0], 3, snowmanPosition[2]+8]
CamFront = [0, 0, -1]
CamZ = [0, 1, 0]
light_color = [1, 1, 1, 1]
day = 1
OpenDoor = -1
doorAngle =0 
lef =0
snowman_direction = -1    
speed = 0.01    
leg_direction = 1
leg2_direction = -1
leg_angle = 0
leg2_angle = 0
def load_texture(filename):
    img = Image.open(filename).transpose(Image.FLIP_TOP_BOTTOM)
    img_data = np.array(list(img.getdata()), np.uint8)
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    return texture




def setup_perspective():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (800/600), 0.1, 90.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(CameraPos[0], CameraPos[1], CameraPos[2], 
              CameraPos[0] + CamFront[0], 
              CameraPos[1] + CamFront[1], 
              CameraPos[2] + CamFront[2], 
              CamZ[0], CamZ[1], CamZ[2])
def process_input(window):
    global CameraPos, CamFront,light_color,day,OpenDoor,doorAngle,leg2_angle,leg2_direction,leg_direction,leg_angle,snowman_direction

    CamSpeed = 0.05  # Adjust as needed
    if glfw.get_key(window, glfw.KEY_W)  == glfw.PRESS:
        CameraPos[2] -= CamSpeed
        CameraPos[0] += CamFront[0] * 0.05
    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        CameraPos[2] += CamSpeed
        CameraPos[0] -= CamFront[0] * 0.1
    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        CameraPos[0] -= CamSpeed
        CameraPos[2] -= CamFront[0] * 0.05
    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        CameraPos[0] += CamSpeed
        CameraPos[2] += CamFront[0] * 0.05
    if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
        CamFront[1] += 0.05
    if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
        CamFront[1] -= 0.05
    if glfw.get_key(window, glfw.KEY_1) == glfw.PRESS :
            light_color = [0,0, 0, 0]
            day = 0
    if glfw.get_key(window, glfw.KEY_2) == glfw.PRESS :
            light_color = [1,1, 1, 1]
            day = 1
   
    if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
        CamFront[0] -= 0.01 
    if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
        CamFront[0] += 0.01 
    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        CameraPos[2] += CamSpeed
    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        CameraPos[0] -= CamSpeed
    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        CameraPos[0] += CamSpeed
    if glfw.get_key(window, glfw.KEY_ENTER) == glfw.PRESS:
        wave()
        rotateHead()
    if glfw.get_key(window, glfw.KEY_G) == glfw.PRESS:
            doorAngle = 90
    if glfw.get_key(window, glfw.KEY_H) == glfw.PRESS:
        doorAngle = 0
    if glfw.get_key(window, glfw.KEY_I)  == glfw.PRESS:
        snowmanPosition[2] -= CamSpeed
        CameraPos[2] -= CamSpeed
        leg_angle += leg_direction * 2
        leg2_angle += leg2_direction * 2
        snowman_direction = -1
       # CameraPos[0] += CamFront[0] * 0.05
    if glfw.get_key(window, glfw.KEY_K) == glfw.PRESS:
        snowmanPosition[2] += CamSpeed
        CameraPos[2] += CamSpeed
        leg2_angle += leg2_direction * 2
        snowman_direction = 1
        #CameraPos[0] -= CamFront[0] * 0.1
        leg_angle += leg_direction * 2
    if glfw.get_key(window, glfw.KEY_J) == glfw.PRESS:
        snowmanPosition[0] -= CamSpeed
        CameraPos[0] -= CamSpeed
        leg_angle += leg_direction * 2
        leg2_angle += leg2_direction * 2
        snowman_direction = 2
        #CameraPos[2] -= CamFront[0] * 0.05
        
    if glfw.get_key(window, glfw.KEY_L) == glfw.PRESS:
        snowmanPosition[0] += CamSpeed
        CameraPos[0] += CamSpeed
        leg_angle += leg_direction * 2
        leg2_angle += leg2_direction * 2
        snowman_direction = -2
        #CameraPos[2] += CamFront[0] * 0.05
def draw_wall(x, y, z, width, height, depth, texture_id):
   
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glEnable(GL_TEXTURE_2D)
    
    glBegin(GL_QUADS)

    glTexCoord2f(0, 0); glVertex3f(x - width/2, y, z - depth/2)
    glTexCoord2f(1, 0); glVertex3f(x + width/2, y, z - depth/2)
    glTexCoord2f(1, 1); glVertex3f(x + width/2, y + height, z - depth/2)
    glTexCoord2f(0, 1); glVertex3f(x - width/2, y + height, z - depth/2)


    glTexCoord2f(0, 0); glVertex3f(x - width/2, y, z + depth/2)
    glTexCoord2f(1, 0); glVertex3f(x + width/2, y, z + depth/2)
    glTexCoord2f(1, 1); glVertex3f(x + width/2, y + height, z + depth/2)
    glTexCoord2f(0, 1); glVertex3f(x - width/2, y + height, z + depth/2)

  
    glTexCoord2f(0, 0); glVertex3f(x - width/2, y, z - depth/2)
    glTexCoord2f(1, 0); glVertex3f(x - width/2, y, z + depth/2)
    glTexCoord2f(1, 1); glVertex3f(x - width/2, y + height, z + depth/2)
    glTexCoord2f(0, 1); glVertex3f(x - width/2, y + height, z - depth/2)

 
    glTexCoord2f(0, 0); glVertex3f(x + width/2, y, z - depth/2)
    glTexCoord2f(1, 0); glVertex3f(x + width/2, y, z + depth/2)
    glTexCoord2f(1, 1); glVertex3f(x + width/2, y + height, z + depth/2)
    glTexCoord2f(0, 1); glVertex3f(x + width/2, y + height, z - depth/2)

    glEnd()
    glBindTexture(GL_TEXTURE_2D, 0)
    glDisable(GL_TEXTURE_2D)



    
def draw_tree(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glPushMatrix()
    glColor3f(0,0.7,0.2)
    glTranslatef(0.0, 1, 0)
    glRotate(-90,1,0,0)
    gluCylinder(gluNewQuadric(), 1.3, 0.0, 1.7, 32, 32)
    glPopMatrix()
    glPushMatrix()
    glColor3f(0.6,0.4,0.2)
    glTranslatef(0.0, -3, 0)
    glRotate(-90,1,0,0)
    gluCylinder(gluNewQuadric(), 0.7, 0.7, 4.2, 32, 32)
    glPopMatrix()
    glPopMatrix()
    

def draw_cube(size):
    glutSolidCube(size)

def draw_pyramid(base, height):
    
    glBegin(GL_TRIANGLES)

  
    glVertex3f(0, height, 0)
    glVertex3f(-base / 2, 0, base / 2)
    glVertex3f(base / 2, 0, base / 2)

    glColor3f(0.6,1,0.9)  
    glVertex3f(0, height, 0)
    glVertex3f(base / 2, 0, base / 2)
    glVertex3f(base / 2, 0, -base / 2)

    glColor3f(0, 1, 0.5)  
    glVertex3f(0, height, 0)
    glVertex3f(base / 2, 0, -base / 2)
    glVertex3f(-base / 2, 0, -base / 2)

    glColor3f(0.6,1,0.9)
    glVertex3f(0, height, 0)
    glVertex3f(-base / 2, 0, -base / 2)
    glVertex3f(-base / 2, 0, base / 2)

    glEnd()

def draw_tower(x,y,z):
   
    glPushMatrix()
    glTranslatef(x, y, z)    

    #Base
    glColor3f(0.9, 0.9, 0.9)                          
    glPushMatrix()                 
    glRotate(-90, 1,0,0)           
                                 
    gluCylinder(gluNewQuadric(), 3, 3, 15, 32, 32)                        
    glPopMatrix()    
    glPushMatrix()
    glColor3f(1, 1, 1)  
    glRotate(-90,0,1,0)                                 
    draw_wall(0,0,3,3,5,0.01, door_texture)
    
    glPopMatrix()

    #roof
    glColor3f(1.0, 0.0, 0.0)                        
    glPushMatrix()                                     
    glTranslatef(0, 14, 0)                           
    glRotatef(-90, 1, 0, 0)   
                       
    glutSolidCone(5, 5, 10, 10)                        
    glPopMatrix()
   
    glPopMatrix()   

def draw_tower2(x,y,z):

    glPushMatrix()
    glTranslatef(x, y, z)                       
    
 
                         
    glPushMatrix()                                   
    glRotate(-90, 1,0,0)                         
    glColor3f(0.6,0.5,0.5)                                  
    gluCylinder(gluNewQuadric(), 3, 3, 10, 10, 10)                                
    glPopMatrix()    
    glPushMatrix()
    glColor3f(1, 1, 1)                                 
    draw_wall(0,0,3,2,3,0.01, door_texture)
    glPopMatrix()
 
    glColor3f(0.4, 0.0, 0.6)                         
    glPushMatrix()                                  
    glTranslatef(0, 9, 0)                             
    glRotatef(-90, 1, 0, 0)                           
    glutSolidCone(5, 5, 10, 10)                       
    glPopMatrix()
    glPopMatrix()   

      
def draw_sofa(width,height,depth,texture):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)

   
    glTexCoord2f(0.0, 0.0); glVertex3f(-width / 2, -height / 2, depth / 2)
    glTexCoord2f(1.0, 0.0); glVertex3f( width / 2, -height / 2, depth / 2)
    glTexCoord2f(1.0, 1.0); glVertex3f( width / 2,  height / 2, depth / 2)
    glTexCoord2f(0.0, 1.0); glVertex3f(-width / 2,  height / 2, depth / 2)

   
    glTexCoord2f(1.0, 0.0); glVertex3f(-width / 2, -height / 2, -depth / 2)
    glTexCoord2f(1.0, 1.0); glVertex3f(-width / 2,  height / 2, -depth / 2)
    glTexCoord2f(0.0, 1.0); glVertex3f( width / 2,  height / 2, -depth / 2)
    glTexCoord2f(0.0, 0.0); glVertex3f( width / 2, -height / 2, -depth / 2)

   
    glTexCoord2f(0.0, 1.0); glVertex3f(-width / 2,  height / 2, -depth / 2)
    glTexCoord2f(0.0, 0.0); glVertex3f(-width / 2,  height / 2,  depth / 2)
    glTexCoord2f(1.0, 0.0); glVertex3f( width / 2,  height / 2,  depth / 2)
    glTexCoord2f(1.0, 1.0); glVertex3f( width / 2,  height / 2, -depth / 2)

  
    glTexCoord2f(1.0, 1.0); glVertex3f(-width / 2, -height / 2, -depth / 2)
    glTexCoord2f(0.0, 1.0); glVertex3f( width / 2, -height / 2, -depth / 2)
    glTexCoord2f(0.0, 0.0); glVertex3f( width / 2, -height / 2,  depth / 2)
    glTexCoord2f(1.0, 0.0); glVertex3f(-width / 2, -height / 2,  depth / 2)

    #Right
    glTexCoord2f(1.0, 0.0); glVertex3f( width / 2, -height / 2, -depth / 2)
    glTexCoord2f(1.0, 1.0); glVertex3f( width / 2,  height / 2, -depth / 2)
    glTexCoord2f(0.0, 1.0); glVertex3f( width / 2,  height / 2,  depth / 2)
    glTexCoord2f(0.0, 0.0); glVertex3f( width / 2, -height / 2,  depth / 2)

    #Left 
    glTexCoord2f(0.0, 0.0); glVertex3f(-width / 2, -height / 2, -depth / 2)
    glTexCoord2f(1.0, 0.0); glVertex3f(-width / 2, -height / 2,  depth / 2)
    glTexCoord2f(1.0, 1.0); glVertex3f(-width / 2,  height / 2,  depth / 2)
    glTexCoord2f(0.0, 1.0); glVertex3f(-width / 2,  height / 2, -depth / 2)

    glEnd()
    glBindTexture(GL_TEXTURE_2D, 0)
    glDisable(GL_TEXTURE_2D)
def draw_house2(x, y, z):
   
    global OpenDoor, doorAngle
    size = 7.0 
    roof_h = 0.5 * size  
    w = 7.0
    h = size
 
    window_size = 2.0
    material([0.8, 0.5, 0.2])
    window_color = (0.1, 0.1, 0.1, 0.4)  
  


    
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotate(-45,0,1,0)


    #furniture
    glPushMatrix()
    glPushMatrix()
    
   
    
  
    glTranslate(0,0,-3)
    draw_sofa(6.5, 0.5, 1,majlis_texture)
   
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0, 0.75, -3.3)
    draw_sofa(6.5, 1, 0.5,majlis_texture)
    
    glPopMatrix()
    
    glPopMatrix()
  


    #roof
    glColor3f(0, 0.3, 0.5)  
    glPushMatrix()
    glTranslatef(0, size/2 , 0) 
    draw_pyramid(size, roof_h)
    glPopMatrix()
   

    glPushMatrix()
    glTranslatef(0, 0, -size / 2)
    draw_rectangle(w, h, 0.1, [0.5, 0.8, 0,1])
    glPopMatrix()

    #Left
    glPushMatrix()
    glTranslatef(-size / 2, 0, 0)
    glRotatef(90, 0, 1, 0) 
    draw_rectangle(w, h, 0.1, [0.2, 0.1, 0,1])
    glPopMatrix()

    #Right
    glPushMatrix()
    glTranslatef(size / 2, 0, 0)
    glRotatef(90, 0, 1, 0) 
    draw_rectangle(w, h, 0.1, [0.2, 0.1, 0,1])
    glPopMatrix()
    glPushMatrix()
    
    glTranslatef(0,h/7,size / 2 )
    if(doorAngle == 90):
        glTranslatef(-window_size/4,  0,0 )
    glRotate(doorAngle,0,1,0)
    draw_rectangle(window_size/2,window_size,0.1, [0,0.4,0.1 ,1])
    glPopMatrix()
    
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glPushMatrix()
    glTranslatef(-size / 3, h/3, size / 2 )  
    draw_rectangle(window_size, window_size, 0.3, window_color)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(size / 3-0.1,  h/3, size / 2 )
    draw_rectangle(window_size, window_size, 0.3, window_color)
    glPopMatrix()
    glPushMatrix()

    #door
    glTranslatef(0,  h/7, size / 2 )
    draw_rectangle(window_size/2,window_size,0.3, [0,0,0 ,0])
    glPopMatrix()
    glDisable(GL_BLEND)
   
    glPushMatrix()

    # Front
    glTranslatef(0, 0, size / 2)
    draw_rectangle(w, h, 0.1, [0.5, 0.8,0,1])
    
    glPopMatrix()
    
    glPopMatrix()
def draw_house(x, y, z):
    
    global OpenDoor, doorAngle
    size = 7.0  
    roof_h = 0.5 * size 
    w = 7.0
    h = size
    house_depth = 7.0
    wall_color = (0.7, 0.7, 1.0)
    window_size = 2.0
    material([0.8, 0.5, 0.2])
    window_color = (0.1, 0.1, 0.1, 0.4)
  


    
    glPushMatrix()
    glTranslatef(x, y, z)
    
    #furniture
    glPushMatrix()
    glPushMatrix()
    
   
    
  
    glTranslate(0,0,-3)
    draw_sofa(6.5, 0.5, 1,majlis_texture)
    
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0, 0.75, -3.3)
    draw_sofa(6.5, 1, 0.5,majlis_texture)
   
    glPopMatrix()
   
    glPopMatrix()
  


   
    glColor3f(1.0, 0.5, 0.5)  
    glPushMatrix()
    glTranslatef(0, size/2 , 0)  
    draw_pyramid(size, roof_h)
    glPopMatrix()
   

 
    glPushMatrix()
    glTranslatef(0, 0, -size / 2)
    draw_rectangle(w, h, 0.1, [0.7, 0.7, 1.0,1])
    glPopMatrix()

    
    glPushMatrix()
    glTranslatef(-size / 2, 0, 0)
    glRotatef(90, 0, 1, 0) 
    draw_rectangle(w, h, 0.1, [0.7, 0.7, 1.0,1])
    glPopMatrix()

   
    glPushMatrix()
    glTranslatef(size / 2, 0, 0)
    glRotatef(90, 0, 1, 0) 
    draw_rectangle(w, h, 0.1, [0.7, 0.7, 1.0,1])
    glPopMatrix()
    glPushMatrix()
    
    glTranslatef(0,h/7,size / 2 )
    if(doorAngle == 90):
        glTranslatef(-window_size/4,  0,0 )
    glRotate(doorAngle,0,1,0)
    draw_rectangle(window_size/2,window_size,0.1, [0,0,0.1 ,1])
    glPopMatrix()
   
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glPushMatrix()
    glTranslatef(-size / 3, h/3, size / 2 ) 
    draw_rectangle(window_size, window_size, 0.3, window_color)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(size / 3-0.1,  h/3, size / 2 )
    draw_rectangle(window_size, window_size, 0.3, window_color)
    glPopMatrix()
    glPushMatrix()

    #door
    glTranslatef(0,  h/7, size / 2 )
    draw_rectangle(window_size/2,window_size,0.3, [0.7,0.4,0.1 ,0])
    glPopMatrix()
    glDisable(GL_BLEND)
   
    glPushMatrix()
    glTranslatef(0, 0, size / 2)
    draw_rectangle(w, h, 0.1, [0.7, 0.7, 1.0,1])
  
    glPopMatrix()
    
    glPopMatrix()

def draw_rectangle(width, height, color):
  
    glColor4f(*color) 
    glBegin(GL_QUADS)
    glVertex3f(-width / 2, -height / 2, 0)
    glVertex3f(width / 2, -height / 2, 0)
    glVertex3f(width / 2, height / 2, 0)
    glVertex3f(-width / 2, height / 2, 0)
    glEnd()

def draw_ground(texture):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-30, 0, -30)
    glTexCoord2f(1, 0); glVertex3f(-30, 0, 30)
    glTexCoord2f(1, 1); glVertex3f(30, 0, 30)
    glTexCoord2f(0, 1); glVertex3f(30, 0, -30)
    glEnd()
    glBindTexture(GL_TEXTURE_2D, 0)
    glDisable(GL_TEXTURE_2D)

def draw_road(x, y, z, width, length, texture_id):
   
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glEnable(GL_TEXTURE_2D)

    glBegin(GL_QUADS)
    
  
    glTexCoord2f(0, 0); glVertex3f(x - width / 2, y, z - length / 2)
    glTexCoord2f(1, 0); glVertex3f(x + width / 2, y, z - length / 2)
    glTexCoord2f(1, 1); glVertex3f(x + width / 2, y, z + length / 2)
    glTexCoord2f(0, 1); glVertex3f(x - width / 2, y, z + length / 2)

    glEnd()
    
    glBindTexture(GL_TEXTURE_2D, 0)
    glDisable(GL_TEXTURE_2D)


def rotateHead():
  
    global headAngle
    global rotationSpeed
    max_head_angle = 90

    print(CameraPos)
    
    if headAngle > -20 :
       headAngle -= rotationSpeed

def wave():
    global armAngle, armDirection

    arm_speed = 2
    max_arm_angle = 45

    armAngle += armDirection * arm_speed
    if armAngle > max_arm_angle or armAngle < -max_arm_angle:
        armDirection *= -1

def draw_human(x, y, z):
 
    glPushMatrix()
    glTranslatef(x, y, z)

    glPushMatrix()
    glRotatef(headAngle, 0, 1, 0)  
    glPushMatrix()
    glTranslatef(0, 1.8, 0) 
    glColor3f(0.8,0.6,0.5)
    glutSolidSphere(0.25, 32, 32) 
    glPopMatrix()

     #eyes
    glColor3f(0, 0, 0)
    glPushMatrix()
    glTranslatef(0.1, 1.9, 0.25)
    glutSolidSphere(0.05, 32, 32)
    glTranslatef(-0.2, 0, 0)
    glutSolidSphere(0.05, 32, 32)
    glPopMatrix()
    glPopMatrix()
 
    glPushMatrix()
    glTranslatef(0, 1.0, 0)
    glScalef(0.7, 1 , 0.5)
    glColor3f(0.6, 0, 0) 
    glutSolidSphere(0.5, 32, 32)
    glPopMatrix()

  
    quadric = gluNewQuadric()

 
    arm_height = 0.6
    glPushMatrix()
    glTranslatef(0.25, 1.3, 0) 
    glRotatef(90, 0, 1, 0) 
    glRotatef(armAngle, 1, 0, 0)
    glColor3f(0.8,0.6,0.5)
    gluCylinder(quadric, 0.05, 0.05, arm_height, 32, 32) 
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.8, 1.3, 0)  
    glRotatef(90, 0, 1, 0)  
    gluCylinder(quadric, 0.05, 0.05, arm_height, 32, 32) 
    glPopMatrix()

   
    leg_height = 1
    glPushMatrix()
    glTranslatef(0.15, 0.7, 0) 
    glRotatef(90, 1, 0, 0)
    gluCylinder(quadric, 0.05, 0.05, leg_height, 32, 32)  
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.15, 0.7, 0)  
    glRotatef(90, 1, 0, 0)
    gluCylinder(quadric, 0.05, 0.05, leg_height, 32, 32)  
    glPopMatrix()

    glPopMatrix()




        
# snowmanPosition = [0, 0, 0]

boo = 0
# def move_snowman():
#     global snowmanPosition, snowman_direction,leg_direction,leg_angle , leg2_angle, leg2_direction
#     max = 45
#     movement= 3
#     leg_angle += leg_direction * movement
#     if leg_angle> max or leg_angle < - max:
#        leg_direction *= -1
#     leg2_angle += leg2_direction * movement
#     if leg_angle> max or leg_angle < - max:
#        leg2_direction *= -1
    

#     snowmanPosition[2] += speed * snowman_direction
    
#     if snowmanPosition[2] > 9 or snowmanPosition[2] < -5: 
#         snowman_direction *= -1
    

#changed to snow man
def draw_snowman():
    global snowman_direction
    glColor3f(1, 1, 1)  

   
    glPushMatrix()
    glTranslatef(snowmanPosition[0], snowmanPosition[1] + 0.65, snowmanPosition[2]) 
    glutSolidSphere(0.4, 20, 20)
    # draw_sphere(0.4, 20, 20)  
    glPopMatrix()

    
    glPushMatrix()
    glTranslatef(snowmanPosition[0], snowmanPosition[1] + 1.1, snowmanPosition[2])  
    if(snowman_direction < 0):
        glRotate(180,0,1,0)
    if(snowman_direction==2):
        glRotate(90,0,1,0)
    if(snowman_direction == -2):
        glRotate(-90,0,1,0)
    # if(snowman_direction < 0):
    #     glRotate(180,0,1,0)
    glutSolidSphere(0.2, 20, 20)
    # draw_sphere(0.2, 20, 20)  
    glColor3f(0, 0, 0)
    glPushMatrix()
    glTranslatef(0.1, 0.1, 0.25)
    glutSolidSphere(0.05, 32, 32)
    glTranslatef(-0.2, 0, 0)
    glutSolidSphere(0.05, 32, 32)
    glPopMatrix()
   
    glPopMatrix()

 
    glColor3f(0.3, 0.3, 0.3) 
    leg_length = 0.4  
    leg_radius = 0.05  

    
    legs = [ (-0.3, 0.15), (0.3, 0.15)]
    global boo
    global lef
    for (x, z) in legs:
        glPushMatrix()
        glTranslatef(snowmanPosition[0] + x, snowmanPosition[1] + 1 - leg_length, snowmanPosition[2] + z)
        glRotatef(90, 1, 0, 0) 
        print(lef)
        if(lef==0):
            glRotatef(leg_angle, 1, 0,0 )
            lef = 1
        elif(lef == 1):
            glRotate(leg2_angle, 1, 0,0 )
            lef = 0
        else: 
            lef += 1
        gluCylinder(gluNewQuadric(), leg_radius, leg_radius, leg_length, 10, 10)
        glPopMatrix()

  
    glColor3f(1, 0.5, 0) 
    glPushMatrix()
    glTranslatef(snowmanPosition[0] - 0.4, snowmanPosition[1] + 0.6, snowmanPosition[2])
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 0.05, 0.05, 0.4, 10, 10) 
    glPopMatrix()

def draw_ear():
  
    glScalef(1, 2, 1)  
    glutSolidCone(0.05, 0.2, 32, 32)

def draw_nose():
    glutSolidSphere(0.05, 32, 32)

def draw_dog(x, y, z):
   
    quadric = gluNewQuadric()
    
    glPushMatrix()
    glTranslatef(x, y, z)

    # Body
    glPushMatrix()
    glColor3f(0.9,0.7,0.4 )  
    glScalef(1.5, 0.7, 0.5)
    glutSolidSphere(0.5, 32, 32)
    glPopMatrix()

    # Head
    glPushMatrix()
    
    glTranslatef(0.5, 0.05, 0)
    glColor3f(0.6, 0.35, 0.05)  
    glPushMatrix()
    glRotatef(90, 0, 1, 0) 
    gluCylinder(quadric, 0.3, 0.0, 0.7, 32, 32)
    glPopMatrix()

    # Ears
    glPushMatrix()
    glTranslatef(0, 0.25, 0.2)
    glColor3f(0.5, 0.35, 0.05)  
    draw_ear()
    glTranslatef(0, 0, -0.4)
    draw_ear()
    glPopMatrix()

    # Nose
    glPushMatrix()
    glTranslatef(0.3, 0, 0)
    draw_nose()
    glPopMatrix()

    # Eyes
    glColor3f(0, 0, 0)  # Black color for the eyes
    glPushMatrix()
    glTranslatef(0.2, 0.1, 0.15)
    glutSolidSphere(0.05, 32, 32)
    glTranslatef(0, 0, -0.3)
    glutSolidSphere(0.05, 32, 32)
    glPopMatrix()

    glColor3f(0.9,0.7,0.4 ) 
    glPopMatrix()

    # Legs
    legs = [(-0.4, -0.22), (0.4, -0.22), (-0.4, 0.22), (0.4, 0.22)]
    for (lx, lz) in legs:
        
        glPushMatrix()
        
        glTranslatef(lx, 0, lz)
        glRotatef(90, 1, 0, 0)
        gluCylinder(quadric, 0.08, 0.08, 0.3, 32, 32)
        
        glPopMatrix()

    # Tail
    glPushMatrix()
    glTranslatef(-0.8, 0, 0)
    glRotatef(45, 0, 1, 0)
    gluCylinder(quadric, 0.05, 0.05, 0.4, 32, 32)
    glPopMatrix()

    glPopMatrix()

glutInit(sys.argv)

def draw_rectangle(width, height, depth, color):
    glColor4f(*color) 
    glPushMatrix()
    glScalef(width, height, depth)
    glutSolidCube(1)
    glPopMatrix()

def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)  
    global light_color
   
    light_position = [1, 1, 1, 0] 
  
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_color)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_color)
    glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT1, GL_POSITION,[10.716999999999924, 3, 8.18200000000001]) # Position of the light
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [1, 1, 0.8, 1]) # Warm light
    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, 0.1)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, 0.05)

def material(color):
    glColor3fv(color)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, color)
   
if not glfw.init():
    raise Exception("GLFW cannot be initialized!")

window = glfw.create_window(800, 600, "OpenGL Window", None, None)
if not window:
    glfw.terminate()
    raise Exception("GLFW window cannot be created!")

glfw.make_context_current(window)



ground_texture = load_texture("grass.jpg")
mountain_texture = load_texture("downloadz.jpg")
wall= load_texture("BACK1.jpg")
road_texture = load_texture("road2.jpg")
majlis_texture = load_texture("Arabian-majlis-furniture.jpg")
door_texture = load_texture("314.jpg")

glEnable(GL_COLOR_MATERIAL)
glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)



global headAngle
headAngle = 80
global armAngle
armAngle = 0
global armDirection
armDirection =1
global rotationSpeed 
rotationSpeed = 0.6

# Main loop
while not glfw.window_should_close(window):
    glfw.poll_events()
    process_input(window) 
    setup_lighting()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    # move_snowman() 
    if leg_angle> 40 or leg_angle < - 40:
       leg_direction *= -1
    if leg_angle> 40 or leg_angle < - 40:
       leg2_direction *= -1
    wallW = 60  
    wallH = 20  
    wallDepth = 0.2  
    glColor3f(1.0, 1.0, 1.0)  
    setup_perspective()
    draw_ground(ground_texture)
       
    road_width = 6.0  
    road_length = 60.0  
    glColor3f(1.0, 1.0, 1.0)
    draw_road(0, 0.01, 0, road_width, road_length, road_texture) 
    draw_snowman()
    glColor3f(1.0, 1.0, 1.0)
    draw_house(-10, 0, 3) 
    material([0.8, 0.5, 0.2]) 
    glPushMatrix()
    draw_house2(8,0,15)
    glPopMatrix()
    draw_human(2, 0, 2)
    draw_tower(10,0,-10)
    draw_tower2(10,0,0)
    glColor3f(1.0, 1.0, 1.0)
    draw_wall(0, 0, -30, wallW, wallH, wallDepth,wall) 
    draw_wall(-30, 0, 0, wallDepth, wallH, wallW,wall)
    draw_wall(30, 0, 0, wallDepth, wallH, wallW,wall)
    draw_dog(4, 0.5, 2)
    draw_tree(-3.7999999999999954, 3, 1.5499999999999647)
    material([0.8, 0.5, 0.2]) 
    
   
    glfw.swap_buffers(window)




glfw.terminate()
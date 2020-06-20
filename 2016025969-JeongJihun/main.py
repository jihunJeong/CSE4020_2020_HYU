import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

gLeftButton = False
gRightButton = False

gFov = 70.
gWidth = 800
gHeight = 800

gCamwith = -0.
gCamHeight = 0.
gPointX = 0.
gPointY = 0.

gXpos = 0
gYpos = 0

cx = 0
cy = 0
cz = 0
time = 0

cbx = 10
cby = 0
cbz = 0

ccx = -10
ccy = 0
ccz = 0

varr = np.array([[0., 0., 0.]], 'float32')
narr = np.array([[0., 0., 0.]], 'float32')
tarr = np.array([[0., 0., 0.]], 'float32')
qarr = np.array([[0., 0., 0.]], 'float32')
marr = np.array([[0., 0., 0.]], 'float32')

aarr = np.array([[0., 0., 0.]], 'float32')
barr = np.array([[0., 0., 0.]], 'float32')
carr = np.array([[0., 0., 0.]], 'float32')
darr = np.array([[0., 0., 0.]], 'float32')
earr = np.array([[0., 0., 0.]], 'float32')

farr = np.array([[0., 0., 0.]], 'float32')
garr = np.array([[0., 0., 0.]], 'float32')
harr = np.array([[0., 0., 0.]], 'float32')
iarr = np.array([[0., 0., 0.]], 'float32')
jarr = np.array([[0., 0., 0.]], 'float32')

gComposedM = np.identity(4)
cameraM = np.identity(4)

gtoggle = [True]

def getCheckSize(v):
    vn = [0, 0, 0]
    for i in range(len(varr)):
        vn[0] = varr[i][0] - v[0]
        vn[1] = varr[i][1] - v[1]
        vn[2] = varr[i][2] - v[2]
        if np.sqrt(np.dot(vn, vn)) <= 1:
            return True
    return False
    
def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([-25,0.,0.]))
    glVertex3fv(np.array([25.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,-25]))
    glVertex3fv(np.array([0.,0.,25.]))
    glEnd()

def drawGrid():
    glBegin(GL_LINES)
    for i in range(-100, 101):
        if i == 0:
            continue

        if i % 10 == 0:
            glColor3ub(100, 100, 100)
        else : 
            glColor3ub(50, 50, 50)
        glVertex3fv(np.array([-25., 0., i/4]))
        glVertex3fv(np.array([25., 0., i/4]))

        glVertex3fv(np.array([i/4, 0., -25.]))
        glVertex3fv(np.array([i/4, 0., 25.]))

    glEnd()

def glDrawArrayA():
    global tarr, qarr, marr

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    
    #draw trianble mesh
    glNormalPointer(GL_FLOAT, 6*tarr.itemsize, tarr)
    glVertexPointer(3, GL_FLOAT, 6*tarr.itemsize, ctypes.c_void_p(tarr.ctypes.data + 3*tarr.itemsize))
    glDrawArrays(GL_TRIANGLES, 0, int(tarr.size/6))
    
    
    #draw quad mesh
    glNormalPointer(GL_FLOAT, 6*qarr.itemsize, qarr)
    glVertexPointer(3, GL_FLOAT, 6*qarr.itemsize, ctypes.c_void_p(qarr.ctypes.data + 3*qarr.itemsize))
    glDrawArrays(GL_QUADS, 0, int(qarr.size/6))
    
    #draw polygon mesh
    glNormalPointer(GL_FLOAT, 6*marr.itemsize, marr)
    glVertexPointer(3, GL_FLOAT, 6*marr.itemsize, ctypes.c_void_p(marr.ctypes.data + 3*marr.itemsize))
    glDrawArrays(GL_POLYGON, 0, int(marr.size/6))


def glDrawArrayB():
    global carr, darr, earr

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    
    #draw trianble mesh
    glNormalPointer(GL_FLOAT, 6*carr.itemsize, carr)
    glVertexPointer(3, GL_FLOAT, 6*carr.itemsize, ctypes.c_void_p(carr.ctypes.data + 3*carr.itemsize))
    glDrawArrays(GL_TRIANGLES, 0, int(carr.size/6))
    
    
    #draw quad mesh
    glNormalPointer(GL_FLOAT, 6*darr.itemsize, darr)
    glVertexPointer(3, GL_FLOAT, 6*darr.itemsize, ctypes.c_void_p(darr.ctypes.data + 3*darr.itemsize))
    glDrawArrays(GL_QUADS, 0, int(darr.size/6))
    
    #draw polygon mesh
    glNormalPointer(GL_FLOAT, 6*earr.itemsize, earr)
    glVertexPointer(3, GL_FLOAT, 6*earr.itemsize, ctypes.c_void_p(earr.ctypes.data + 3*earr.itemsize))
    glDrawArrays(GL_POLYGON, 0, int(earr.size/6))

def glDrawArrayC():
    global harr, iarr, jarr

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    
    #draw trianble mesh
    glNormalPointer(GL_FLOAT, 6*harr.itemsize, harr)
    glVertexPointer(3, GL_FLOAT, 6*harr.itemsize, ctypes.c_void_p(harr.ctypes.data + 3*harr.itemsize))
    glDrawArrays(GL_TRIANGLES, 0, int(harr.size/6))
    
    
    #draw quad mesh
    glNormalPointer(GL_FLOAT, 6*iarr.itemsize, iarr)
    glVertexPointer(3, GL_FLOAT, 6*iarr.itemsize, ctypes.c_void_p(iarr.ctypes.data + 3*iarr.itemsize))
    glDrawArrays(GL_QUADS, 0, int(darr.size/6))
    
    #draw polygon mesh
    glNormalPointer(GL_FLOAT, 6*jarr.itemsize, earr)
    glVertexPointer(3, GL_FLOAT, 6*jarr.itemsize, ctypes.c_void_p(earr.ctypes.data + 3*jarr.itemsize))
    glDrawArrays(GL_POLYGON, 0, int(jarr.size/6))

def render():
    global gComposedM, cameraM, cx, cy, cz 
    global cbx, cby, cbz, ccx, ccy, ccz
    cx = gComposedM[0][3]
    cy = gComposedM[1][3]
    cz = gComposedM[2][3]
    
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if gtoggle[0]:
        gluPerspective(gFov, gWidth/gHeight, 5, 1000)
        gluLookAt(cx+20, cy+20, cz+20, cx, cy, cz, 0,.1,0)
    else :
        gluPerspective(100, gWidth/gHeight, 5, 1000)
        glMultMatrixf(cameraM)
        gluLookAt(cx, cy, cz+1, cx, cy, cz+2, 0,.1,0)
        
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    
    glTranslatef(gPointX, 0, 0)
    glTranslatef(0, gPointY, 0)
    glRotatef(gCamHeight, 1, 0, 0)
    glRotatef(gCamwith, 0, 1, 0)
    

    drawFrame()
    drawGrid()

    glEnable(GL_LIGHTING)   # try to uncomment: no lighting
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)

    glEnable(GL_NORMALIZE)  # try to uncomment: lighting will be incorrect if you scale the object
    
    # glEnable(GL_RESCALE_NORMAL)
    ambientLightColor = (.1,.1,.1,1.)
    
    glPushMatrix()
    S = np.identity(4)
    S[:3, :3] = np.array([[np.cos(time), -np.sin(time), 0],
                      [np.sin(time), np.cos(time), 0],
                      [0.,0.,1.]])
    glMultMatrixf(S.T)
    #White Light position 1
    WhitelightPos = (1000, 0., 1000, 1.)
    WhitelightColor = (0.75, 0, 0.75, 1.)
    glLightfv(GL_LIGHT0, GL_POSITION, WhitelightPos)
    glPopMatrix()

    # light intensity for each color channels
    glLightfv(GL_LIGHT0, GL_DIFFUSE, WhitelightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, WhitelightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)
  
    #White Light position 2
    WhitelightPos = (1000.,0.,1000.,1.)
    WhitelightColor = (0.75, 0.75, 0.75, 0.1)
    glLightfv(GL_LIGHT1, GL_POSITION, WhitelightPos)

    # light intensity for each color channels
    glLightfv(GL_LIGHT1, GL_DIFFUSE, WhitelightColor)
    glLightfv(GL_LIGHT1, GL_SPECULAR, WhitelightColor)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor)

    specularObjectColor = (1.,1.,1.,1.)
    # material reflectance for each color channel
    objectColor = (1.,1.,0.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)

    glPushMatrix()
    glMultMatrixf(gComposedM.T)
    glDrawArrayA()
    glPopMatrix()

    glPushMatrix()
    v1 = [cx - cbx, cy - cby, cz - cbz]
    v2 = [cbx - ccx, cby - ccy, cbz - ccz]
    v3 = [ccx - cx, ccy - cy, ccz - cz]

    if getCheckSize([cbx, cby, cbz]):
        cbx = 8 * np.cos(time)
        cby = 4 * np.sin(time) + 4 * np.cos(time)
        cbz = 8 * np.sin(time)
        if np.sqrt(np.dot(v2, v2)) <= 5:
            cbx = -2 * ccx - 2
    glTranslatef(cbx, cby, cbz)
    # material reflectance for each color channel
    objectColor = (0.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glDrawArrayB()
    glPopMatrix()

    glPushMatrix()
    if getCheckSize([ccx, ccy, ccz]):
        ccx = 8 * np.cos(4 * time)
        ccy = 4 * np.sin(2 * time) + 4 * np.cos(2 * time)
        ccz = 8 * np.sin(3 * time)
        if np.sqrt(np.dot(v2, v2)) <= 5:
            ccx = -1 * ccx -2
    glTranslatef(ccx, ccy, ccz)
    # material reflectance for each color channel
    objectColor = (1.,0.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glDrawArrayC()
    glPopMatrix()

    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    glDisable(GL_LIGHTING)

def mouse_button_callback(window, button, action, mods):
    global gLeftButton, gRightButton
    if action == glfw.PRESS or action == glfw.REPEAT:
        if button == glfw.MOUSE_BUTTON_LEFT:
            gLeftButton = True
        elif button == glfw.MOUSE_BUTTON_RIGHT:
            gRightButton = True
    else :
        gLeftButton = False
        gRightButton = False


def cursor_position_callback(window, xoffset, yoffset):
    global gCamwith, gCamHeight, gLeftButton, gRightButton
    global gXpos, gYpos, gPointX, gPointY
    changedX = gXpos - xoffset
    changedY = gYpos - yoffset
    
    if gLeftButton == True and gRightButton == False:
        gCamwith -= 5 *np.radians(changedX)
        gCamHeight -= 5 * np.radians(changedY)

    if gRightButton == True and gLeftButton == False:
        gPointX -= 0.005*changedX
        gPointY += 0.005*changedY

    gXpos = xoffset
    gYpos = yoffset


def scroll_callback(window, xoffset, yoffset):
    global gFov, gLeftButton, gComposedM
    
    scalar = 1
    if yoffset < 0:
        scalar = scalar / (-1 * yoffset * 1.2)
    else :
        scalar = (yoffset * 1.2)

    nM = np.identity(4)
    if gLeftButton and not gRightButton:
        nM[:3, :3] = [[scalar, 0, 0],
                     [0, scalar, 0],
                     [0, 0, scalar]]
        gComposedM = gComposedM @ nM
    else :
        gFov -= yoffset

def key_callback(window, key, scancode, action, mods):
    global gComposedM, cameraM, gLeftButton, gRightButton
    global cx, cy, cz

    nM = np.identity(4)
    cM = np.identity(4)
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key == glfw.KEY_D and not gLeftButton and not gRightButton:
            #X minus Transition
            nM[0][3] = -0.3
        elif key == glfw.KEY_A and not gLeftButton and not gRightButton:
            #X plus transition
            nM[0][3] = 0.3
        elif key == glfw.KEY_Q and not gLeftButton and not gRightButton:
            #Y minus Transition
            nM[1][3] = -0.3
        elif key == glfw.KEY_E and not gLeftButton and not gRightButton:
            #Y plus transition
            nM[1][3] = 0.3
        elif key == glfw.KEY_S and not gLeftButton and not gRightButton:
            #Z minus Transition
            nM[2][3] = -0.3
        elif key == glfw.KEY_W and not gLeftButton and not gRightButton:
            #Z plus transition
            nM[2][3] = 0.3
        elif key == glfw.KEY_D and gLeftButton and not gRightButton:
            #Y axis minus Rotation
            th = np.radians(-10)
            nM[:3, :3] = [[np.cos(th), 0, np.sin(th)],
                          [0, 1, 0],
                          [-np.sin(th), 0, np.cos(th)]]
            th = np.radians(-10)
            cM[:3, :3] = [[np.cos(th), 0, np.sin(th)],
                          [0, 1, 0],
                          [-np.sin(th), 0, np.cos(th)]]
        elif key == glfw.KEY_A and gLeftButton and not gRightButton:
            #Y axis plus Rotation
            th = np.radians(10)
            nM[:3, :3] = [[np.cos(th), 0, np.sin(th)],
                         [0, 1, 0],
                         [-np.sin(th), 0, np.cos(th)]]
            th = np.radians(10)
            cM[:3, :3] = [[np.cos(th), 0, np.sin(th)],
                         [0, 1, 0],
                         [-np.sin(th), 0, np.cos(th)]]
        elif key == glfw.KEY_S and gLeftButton and not gRightButton:
            #X axis minus Rotation
            th = np.radians(-10)
            nM[:3, :3] = [[1, 0, 0],
                         [0, np.cos(th), -np.sin(th)],
                         [0, np.sin(th), np.cos(th)]]
            th = np.radians(10)
            cM[:3, :3] = [[1, 0, 0],
                         [0, np.cos(th), -np.sin(th)],
                         [0, np.sin(th), np.cos(th)]]
        elif key == glfw.KEY_W and gLeftButton and not gRightButton:
            #X axis plus Rotation
            th = np.radians(10)
            nM[:3, :3] = [[1, 0, 0],
                         [0, np.cos(th), -np.sin(th)],
                         [0, np.sin(th), np.cos(th)]]
            th = np.radians(-10)
            cM[:3, :3] = [[1, 0, 0],
                         [0, np.cos(th), -np.sin(th)],
                         [0, np.sin(th), np.cos(th)]]
        elif key == glfw.KEY_Q and gLeftButton and not gRightButton:
            #Z axis minus Rotation
            th = np.radians(-10)
            nM[:3, :3] = [[np.cos(th), -np.sin(th), 0],
                         [np.sin(th), np.cos(th), 0],
                         [0, 0, 1]]
            th = np.radians(10)
            cM[:3, :3] = [[np.cos(th), -np.sin(th), 0],
                         [np.sin(th), np.cos(th), 0],
                         [0, 0, 1]]
        elif key == glfw.KEY_E and gLeftButton and not gRightButton:
            #Z axis plus Rotation
            th = np.radians(10)
            nM[:3, :3] = [[np.cos(th), -np.sin(th), 0],
                         [np.sin(th), np.cos(th), 0],
                         [0, 0, 1]]
            th = np.radians(-10)
            cM[:3, :3] = [[np.cos(th), -np.sin(th), 0],
                         [np.sin(th), np.cos(th), 0],
                         [0, 0, 1]]
        elif key == glfw.KEY_D and not gLeftButton and gRightButton:
            #X minus Shere
            nM[:3, :3] = [[1, -0.1, 0],
                         [0, 1, 0],
                         [0.,0.,1.]]
        elif key == glfw.KEY_A and not gLeftButton and gRightButton:
            #X plus Shere
            nM[:3, :3] = [[1, 0.1, 0],
                         [0, 1, 0],
                         [0.,0.,1.]]
        elif key == glfw.KEY_Q and not gLeftButton and gRightButton:
            #Z minus Shere
            nM[:3, :3] = [[1., 0., 0.],
                         [0., 1., 0.],
                         [0,-0.1,1.]]
        elif key == glfw.KEY_E and not gLeftButton and gRightButton:
            #Z plus Shere
            nM[:3, :3] = [[1, 0, 0],
                         [0, 1, 0],
                         [0,0.1,1.]]
        elif key == glfw.KEY_Z :
            #X Reflection
            gComposedM[0][3] = gComposedM[0][3] * -1
        elif key == glfw.KEY_X :
            #Y Reflection
            gComposedM[1][3] = gComposedM[1][3] * -1
        elif key == glfw.KEY_C :
            #Z Reflection
            gComposedM[2][3] = gComposedM[2][3] * -1
        elif key == glfw.KEY_V :
            gtoggle[0] = not gtoggle[0]

        gComposedM = gComposedM @ nM
        cameraM = cameraM @ cM

        
def draw_imageA():
    global varr, narr, tarr, qarr, marr 
    
    #Open obj file
    f = open('./obj/LowPolyFiatUNO.obj', 'r')

    while True:
        line = f.readline()
        if not line:
            break

        input_list = list(line.split())
        if len(input_list) < 2:
            continue

        if input_list[0] == "v":
            varr = np.append(varr, np.array([[float(input_list[1]), float(input_list[2]), float(input_list[3])]], 'float32'), axis=0)
        elif input_list[0] == "vn":
            narr = np.append(narr, np.array([[float(input_list[1]), float(input_list[2]), float(input_list[3])]], 'float32'), axis=0)
        elif input_list[0] == "f":
            if input_list[len(input_list)-1] == '\n':
                input_list = np.delete(input_list, len(input_list)-1,0)

            #Count number of faces to print 
            if len(input_list) == 4:
                for i in range(1,4):
                    sli = input_list[i].split('/')
                    if len(sli) < 3:
                        tarr = np.append(tarr, np.array([varr[int(sli[0])]], 'float32'), axis=0)
                    else :
                        tarr = np.append(tarr, np.array([narr[int(sli[2])]], 'float32'), axis=0)
                    tarr = np.append(tarr, np.array([varr[int(sli[0])]], 'float32'), axis=0)

            elif len(input_list) == 5:
                for i in range(1,5):
                    sli = input_list[i].split('/')
                    if len(sli) < 3:
                        qarr = np.append(qarr, np.array([varr[int(sli[0])]], 'float32'), axis=0)
                    else :
                        qarr = np.append(qarr, np.array([narr[int(sli[2])]], 'float32'), axis=0)
                    qarr = np.append(qarr, np.array([varr[int(sli[0])]], 'float32'), axis=0)

            if len(input_list) > 5:
                for i in range(1, len(input_list)):
                    sli = input_list[i].split('/')
                    if len(sli) < 3:
                        marr = np.append(marr, np.array([varr[int(sli[0])]], 'float32'), axis=0)
                    else :
                        marr = np.append(marr, np.array([narr[int(sli[2])]], 'float32'), axis=0)
                    marr = np.append(marr, np.array([varr[int(sli[0])]], 'float32'), axis=0)

    f.close()
    varr = np.delete(varr, [0], axis=0)
    tarr = np.delete(tarr, [0], axis=0)
    qarr = np.delete(qarr, [0], axis=0)
    marr = np.delete(marr, [0], axis=0)

def draw_imageB():
    global aarr, barr, carr, darr, earr 
    
    #Open obj file
    f = open('./obj/LowPolyFiatUNO.obj', 'r')

    while True:
        line = f.readline()
        if not line:
            break

        input_list = list(line.split())
        if len(input_list) < 2:
            continue

        if input_list[0] == "v":
            aarr = np.append(aarr, np.array([[float(input_list[1]), float(input_list[2]), float(input_list[3])]], 'float32'), axis=0)
        elif input_list[0] == "vn":
            barr = np.append(barr, np.array([[float(input_list[1]), float(input_list[2]), float(input_list[3])]], 'float32'), axis=0)
        elif input_list[0] == "f":
            if input_list[len(input_list)-1] == '\n':
                input_list = np.delete(input_list, len(input_list)-1,0)

            if len(input_list) == 4:
                for i in range(1,4):
                    sli = input_list[i].split('/')
                    if len(sli) < 3:
                        carr = np.append(carr, np.array([aarr[int(sli[0])]], 'float32'), axis=0)
                    else :
                        carr = np.append(carr, np.array([barr[int(sli[2])]], 'float32'), axis=0)
                    carr = np.append(carr, np.array([aarr[int(sli[0])]], 'float32'), axis=0)

            elif len(input_list) == 5:
                for i in range(1,5):
                    sli = input_list[i].split('/')
                    if len(sli) < 3:
                        darr = np.append(darr, np.array([aarr[int(sli[0])]], 'float32'), axis=0)
                    else :
                        darr = np.append(darr, np.array([barr[int(sli[2])]], 'float32'), axis=0)
                    darr = np.append(darr, np.array([aarr[int(sli[0])]], 'float32'), axis=0)

            if len(input_list) > 5:
                for i in range(1, len(input_list)):
                    sli = input_list[i].split('/')
                    if len(sli) < 3:
                        earr = np.append(earr, np.array([aarr[int(sli[0])]], 'float32'), axis=0)
                    else :
                        earr = np.append(earr, np.array([barr[int(sli[2])]], 'float32'), axis=0)
                    earr = np.append(earr, np.array([aarr[int(sli[0])]], 'float32'), axis=0)

    f.close()
    carr = np.delete(carr, [0], axis=0)
    darr = np.delete(darr, [0], axis=0)
    earr = np.delete(earr, [0], axis=0)

def draw_imageC():
    global farr, garr, harr, iarr, jarr 
    
    #Open obj file
    f = open('./obj/Futuristic_Car_2.1_obj.obj', 'r')

    while True:
        line = f.readline()
        if not line:
            break

        input_list = list(line.split())
        if len(input_list) < 2:
            continue

        if input_list[0] == "v":
            farr = np.append(farr, np.array([[float(input_list[1]), float(input_list[2]), float(input_list[3])]], 'float32'), axis=0)
        elif input_list[0] == "vn":
            garr = np.append(garr, np.array([[float(input_list[1]), float(input_list[2]), float(input_list[3])]], 'float32'), axis=0)
        elif input_list[0] == "f":
            if input_list[len(input_list)-1] == '\n':
                input_list = np.delete(input_list, len(input_list)-1,0)

            #Count number of faces to print 
            if len(input_list) == 4:
                for i in range(1,4):
                    sli = input_list[i].split('/')
                    if len(sli) < 3:
                        harr = np.append(harr, np.array([farr[int(sli[0])]], 'float32'), axis=0)
                    else :
                        harr = np.append(harr, np.array([garr[int(sli[2])]], 'float32'), axis=0)
                    harr = np.append(harr, np.array([farr[int(sli[0])]], 'float32'), axis=0)

            elif len(input_list) == 5:
                for i in range(1,5):
                    sli = input_list[i].split('/')
                    if len(sli) < 3:
                        iarr = np.append(iarr, np.array([farr[int(sli[0])]], 'float32'), axis=0)
                    else :
                        iarr = np.append(iarr, np.array([garr[int(sli[2])]], 'float32'), axis=0)
                    iarr = np.append(iarr, np.array([farr[int(sli[0])]], 'float32'), axis=0)

            if len(input_list) > 5:
                for i in range(1, len(input_list)):
                    sli = input_list[i].split('/')
                    if len(sli) < 3:
                        jarr = np.append(jarr, np.array([farr[int(sli[0])]], 'float32'), axis=0)
                    else :
                        jarr = np.append(jarr, np.array([garr[int(sli[2])]], 'float32'), axis=0)
                    jarr = np.append(jarr, np.array([farr[int(sli[0])]], 'float32'), axis=0)

    f.close()
    harr = np.delete(harr, [0], axis=0)
    iarr = np.delete(iarr, [0], axis=0)
    jarr = np.delete(jarr, [0], axis=0)

def size_callback(window, width, height):
    global gWidth, gHeight
    gWidth = width
    gHeight = height
    glViewport(0, 0, gWidth, gHeight)

def main():
    global gVertexArrayIndexed, gIndexArray, time

    if not glfw.init():
        return
    window = glfw.create_window(640,640,'2016025969', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)

    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_cursor_pos_callback(window, cursor_position_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_key_callback(window, key_callback)
    glfw.set_framebuffer_size_callback(window, size_callback)
    draw_imageA()
    draw_imageB()
    draw_imageC()
    #glfw.set_drop_callback(window, drop_callback)

    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        time = glfw.get_time()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
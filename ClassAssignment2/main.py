import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

gLeftButton = False
gRightButton = False
gFov = 150.
gCamwith = -45.
gCamHeight = 50.
gPointX = 0.
gPointY = 0.
gXpos = 0
gYpos = 0

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

def createVertexAndIndexArrayIndexed():
    varr = np.array([
            (-0.5773502691896258, 0.5773502691896258, 0.5773502691896258),
            ( -1 ,  1 ,  1 ), # v0
            (0.8164965809277261, 0.4082482904638631, 0.4082482904638631),
            (  1 ,  1 ,  1 ), # v1
            (0.4082482904638631, -0.4082482904638631, 0.8164965809277261),
            (  1 , -1 ,  1 ), # v2
            (-0.4082482904638631, -0.8164965809277261, 0.4082482904638631),
            ( -1 , -1 ,  1 ), # v3
            (-0.4082482904638631, 0.4082482904638631, -0.8164965809277261),
            ( -1 ,  1 , -1 ), # v4
            (0.4082482904638631, 0.8164965809277261, -0.4082482904638631),
            (  1 ,  1 , -1 ), # v5
            (0.5773502691896258, -0.5773502691896258, -0.5773502691896258),
            (  1 , -1 , -1 ), # v6
            (-0.8164965809277261, -0.4082482904638631, -0.4082482904638631),
            ( -1 , -1 , -1 ), # v7
            ], 'float32')
    iarr = np.array([
            (0,2,1),
            (0,3,2),
            (4,5,6),
            (4,6,7),
            (0,1,5),
            (0,5,4),
            (3,6,2),
            (3,7,6),
            (1,2,6),
            (1,6,5),
            (0,7,3),
            (0,4,7),
            ])
    return varr, iarr

def drawCube_glDrawElements():
    global gVertexArrayIndexed, gIndexArray
    varr = gVertexArrayIndexed
    iarr = gIndexArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6 * varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)

def render():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(gFov, 1, 1, 10)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    gluLookAt(0, 0, 4, 0,0,0, 0,.1,0)

    glTranslatef(gPointX, 0, 0)
    glTranslatef(0, gPointY, 0)
    glRotatef(gCamHeight, 1, 0, 0)
    glRotatef(gCamwith, 0, 1, 0)
 
    drawFrame()
    drawGrid()

    glColor3ub(255, 255, 255)
    

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
    global gFov
    gFov -= 3*yoffset;
    if gFov <= 1:
    	gFov = 1
    elif gFov >= 175:
    	gFov = 175

def drop_callback(window, paths):
	paths = str(paths)
	f = open(paths[2:-2], 'r')
	vtx_cnt = 0
	while True:
		line = f.readline()
		if not line:
			break
		print(line)
		input_list = list(line.split())

		if input_list[0] == "v":
			varr.append(list(map(int, input_list[1:])))
	f.close()

gVertexArrayIndexed = None
gIndexArray = None

def main():
	global gVertexArrayIndexed, gIndexArray

    if not glfw.init():
        return
    window = glfw.create_window(480,480,'2016025969', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)

    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_cursor_pos_callback(window, cursor_position_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_drop_callback(window, drop_callback)

    gVertexArrayIndexed, gIndexArray = createVertexAndIndexArrayIndexed()
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()

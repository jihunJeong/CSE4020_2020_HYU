import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

gLeftButton = False
gRightButton = False
gFov = 130.
gCamwith = -45.
gCamHeight = 50.
gPointX = 0.
gPointY = 0.
gXpos = 0
gYpos = 0

# draw a cube of side 1, centered at the origin.
def drawUnitCube():
    glBegin(GL_QUADS)
    glVertex3f( 0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f( 0.5, 0.5, 0.5) 
                             
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f( 0.5,-0.5,-0.5) 
                             
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
                             
    glVertex3f( 0.5,-0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f( 0.5, 0.5,-0.5)
 
    glVertex3f(-0.5, 0.5, 0.5) 
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5) 
    glVertex3f(-0.5,-0.5, 0.5) 
                             
    glVertex3f( 0.5, 0.5,-0.5) 
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5,-0.5)
    glEnd()

def drawCubeArray(xwidth=0.5, ywidth=0.5, zwidth=0.5):
    glPushMatrix()
    glScalef(xwidth,ywidth,zwidth)
    drawUnitCube()
    glPopMatrix()

def drawSphere(numLats=12, numLongs=12):
	for i in range(0, numLats+1):
		lat0 =np.pi * (-0.5 + float(float(i - 1) / float(numLats)))
		z0 = np.sin(lat0)
		zr0 = np.cos(lat0)

		lat1 = np.pi * (-0.5 + float(float(i) / float(numLats)))
		z1 = np.sin(lat1)
		zr1 = np.cos(lat1)

		glBegin(GL_POLYGON)

		for j in range(0, numLongs +1):
			lng = 2 * np.pi * float(float(j - 1) / float(numLongs))
			x = np.cos(lng)
			y = np.sin(lng)
			glVertex3f(0.1*(x * zr0), 0.1*(y * zr0), 0.1*(z0))
			glVertex3f(0.1*(x * zr1), 0.1*(y * zr1), 0.1*(z1))

		glEnd()


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

def drawPeople():
	t = glfw.get_time()	

	#draw hips
	glPushMatrix()
	glTranslatef(0, 2.3, 0)
	glTranslatef(0, 0, 0.25*t)
	drawCubeArray(0.3, 0.1, 0.3)

	#draw left upper legs
	glPushMatrix()
	glTranslatef(0.3, -0.8, 0)
	glRotatef(-20, 1, 0, 0)
	glRotatef(np.sin(7*t)*30, 1, 0, 0)
	drawCubeArray(0.3, 1.0, 0.3)

	#draw left lower legs
	glPushMatrix()
	glTranslatef(0, -1., -0.5)
	glRotatef(30, 1, 0, 0)
	glRotatef(np.sin(7*t)*45+30, 1, 0, 0)
	drawCubeArray(0.3, 0.8, 0.3)
	glTranslatef(0, -0.5, 0.3)
	drawCubeArray(0.3, 0.3, 0.3)
	glPopMatrix()
	glPopMatrix()

	#draw right upper legs
	glPushMatrix()
	glTranslatef(-0.3, -0.8, 0)
	glRotatef(-20, 1, 0, 0)
	glRotatef(-np.sin(7*t)*30, 1, 0, 0)
	drawCubeArray(0.3, 1.0, 0.3)

	#draw right lower legs
	glPushMatrix()
	glTranslatef(0, -1.0, -0.5)
	glRotatef(30, 1, 0, 0)
	glRotatef(-np.sin(7*t)*45+30 ,1, 0, 0)
	drawCubeArray(0.3, 0.8, 0.3)
	glTranslatef(0, -0.5, 0.3)
	drawCubeArray(0.3, 0.3, 0.3)
	glPopMatrix()
	glPopMatrix()

	#draw body
	glTranslatef(0, 0.7, 0)
	drawCubeArray(0.3, 0.8, 0.3)

	#draw left upper arms
	glPushMatrix()
	glTranslatef(0.4, 0.15, 0)
	glRotatef(30, 1, 0, 0)
	#glRotatef(t*(180/np.pi), 1, 0, 0)
	drawCubeArray(0.15, 0.5, 0.15)

	#draw left lower arms
	glPushMatrix()
	glTranslatef(0, -0.6, 0)
	drawCubeArray(0.15, 0.5, 0.15)
	glPopMatrix()
	glPopMatrix()

	#draw right upper arms
	glPushMatrix()
	glTranslatef(-0.4, 0.15, 0)
	glRotatef(-30, 1, 0, 0)
	drawCubeArray(0.15, 0.5, 0.15)

	#draw right lower arms
	glPushMatrix()
	glTranslatef(0, -0.6, 0)
	drawCubeArray(0.15, 0.5, 0.15)
	glPopMatrix()
	glPopMatrix()

	#draw head
	glPushMatrix()
	glTranslatef(0, 0.55, 0)
	drawSphere()
	glPopMatrix()

	glPopMatrix()


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
    drawPeople()


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


def scroll_callback(windw, xoffset, yoffset):
    global gFov
    gFov -= 3*yoffset;
    if gFov <= 1:
    	gFov = 1


def main():
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

    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()

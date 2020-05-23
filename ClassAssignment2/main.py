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
varr = np.array([[0., 0., 0.]], 'float32')
narr = np.array([[0., 0., 0.]], 'float32')
tarr = np.array([[0., 0., 0.]], 'float32')
qarr = np.array([[0., 0., 0.]], 'float32')
marr = np.array([[0., 0., 0.]], 'float32')
gtoggle = [True, False]

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

def createVertexArraySeparate():
	global tarr, qarr, marr, varr, narr

	return tarr

def glDrawArray():
    global varr, narr, tarr, qarr, marr, gtoggle

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
    
def render():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    #set Toggle wireframe / solid by pressing Z key
    if gtoggle[0]:
    	glPolygonMode( GL_FRONT_AND_BACK, GL_LINE)
    else :
    	glPolygonMode( GL_FRONT_AND_BACK, GL_FILL)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(gFov, 1, 1, 10)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    gluLookAt(0, 0, 8, 0,0,0, 0,.1,0)

    glTranslatef(gPointX, 0, 0)
    glTranslatef(0, gPointY, 0)
    glRotatef(gCamHeight, 1, 0, 0)
    glRotatef(gCamwith, 0, 1, 0)
 
    drawFrame()
    drawGrid()

    glEnable(GL_LIGHTING)   # try to uncomment: no lighting
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)
    glEnable(GL_LIGHT3)

    glEnable(GL_NORMALIZE)  # try to uncomment: lighting will be incorrect if you scale the object
    # glEnable(GL_RESCALE_NORMAL)

    # Red light position
    ambientLightColor = (.1,.1,.1,1.)

    RedlightPos = (0.,np.sqrt(10**3),0.,1.)    # try to change 4th element to 0. or 1.
    RedColor = (1.,0.2,0.2,1.)
    glLightfv(GL_LIGHT0, GL_POSITION, RedlightPos)
	# light intensity for each color channel
    glLightfv(GL_LIGHT0, GL_DIFFUSE, RedColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, RedColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)
    #Green light position
    
    GreenlightPos = (-10.,-10.,10.,1.)    # try to change 4th element to 0. or 1.
    GreenlightColor = (0.2,1.,0.2,1.)
    glLightfv(GL_LIGHT1, GL_POSITION, GreenlightPos)
    
    # light intensity for each color channel
    glLightfv(GL_LIGHT1, GL_DIFFUSE, GreenlightColor)
    glLightfv(GL_LIGHT1, GL_SPECULAR, GreenlightColor)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor)
    #BLue light position
    
    BluelightPos = (10.,-10.,-10.,1.)    # try to change 4th element to 0. or 1.
    BluelightColor = (0.2,0.2,1.,1.)
    glLightfv(GL_LIGHT2, GL_POSITION, BluelightPos)
   	
   	# light intensity for each color channel
    glLightfv(GL_LIGHT2, GL_DIFFUSE, BluelightColor)
    glLightfv(GL_LIGHT2, GL_SPECULAR, BluelightColor)
    glLightfv(GL_LIGHT2, GL_AMBIENT, ambientLightColor)

    #White Light position
    WhitelightPos = (10.,0.,10.,1.)
    WhitelightColor = (0.75, 0.75, 0.75, 0.1)
    glLightfv(GL_LIGHT3, GL_POSITION, WhitelightPos)

	# light intensity for each color channel
    glLightfv(GL_LIGHT3, GL_DIFFUSE, WhitelightColor)
    glLightfv(GL_LIGHT3, GL_SPECULAR, WhitelightColor)
    glLightfv(GL_LIGHT3, GL_AMBIENT, ambientLightColor)

    glColor3ub(255, 255, 255)
    glDrawArray()

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
    global gFov
    gFov -= 3*yoffset;
    if gFov <= 1:
    	gFov = 1
    elif gFov >= 175:
    	gFov = 175

def key_callback(window, key, scancode, action, mods):
	global gtoggle

	if action==glfw.PRESS or action==glfw.REPEAT:
		if key == glfw.KEY_Z:
			#Set toggle switch for glPolygon
			gtoggle[0] = not gtoggle[0]
		elif key == glfw.KEY_S:
			gtoggle[1] = not gtoggle[1]

def drop_callback(window, paths):
	global varr, narr, tarr, qarr, marr

	varr = np.array([[0., 0., 0.]], 'float32')
	narr = np.array([[0., 0., 0.]], 'float32')
	tarr = np.array([[0., 0., 0.]], 'float32')
	qarr = np.array([[0., 0., 0.]], 'float32')
	marr = np.array([[0., 0., 0.]], 'float32')
	
	#Get paths to read obj files and  file name
	paths = str(paths)
	file_name = list(paths.split('/'))[-1][:-2]
	
	#Open obj file
	f = open(paths[2:-2], 'r')
	count3F, count4F, countMF = 0, 0, 0

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
				count3F += 1
				for i in range(1,4):
					sli = input_list[i].split('/')
					if len(sli) < 3:
						tarr = np.append(tarr, np.array([varr[int(sli[0])]], 'float32'), axis=0)
					else :
						tarr = np.append(tarr, np.array([narr[int(sli[2])]], 'float32'), axis=0)
					tarr = np.append(tarr, np.array([varr[int(sli[0])]], 'float32'), axis=0)

			elif len(input_list) == 5:
				count4F += 1
				for i in range(1,5):
					sli = input_list[i].split('/')
					if len(sli) < 3:
						qarr = np.append(qarr, np.array([varr[int(sli[0])]], 'float32'), axis=0)
					else :
						qarr = np.append(qarr, np.array([narr[int(sli[2])]], 'float32'), axis=0)
					qarr = np.append(qarr, np.array([varr[int(sli[0])]], 'float32'), axis=0)

			if len(input_list) > 5:
				countMF += 1
				for i in range(32):
					marr = np.append(marr, np.array([narr[sli[i][1]]], 'float32'), axis=0)
					marr = np.append(marr, np.array([varr[sli[i][0]]], 'float32'), axis=0)
				
	f.close()
	tarr = np.delete(tarr, [0], axis=0)
	qarr = np.delete(qarr, [0], axis=0)
	marr = np.delete(marr, [0], axis=0)
				
	#Print out the information of the obj file to console
	print()
	print("=================================================================")
	print("File name : " + file_name)
	print("Total number of faces : ", (count3F+count4F+countMF))
	print("Number of faces with 3 vertics : ", (count3F))
	print("Number of faces with 4 vertics : ", (count4F))
	print("Number of faces with more than 4 vertics : ", (countMF))
	print("=================================================================")

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
    glfw.set_key_callback(window, key_callback)
    glfw.set_drop_callback(window, drop_callback)

    glfw.swap_interval(1)
    tarr = createVertexArraySeparate()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()

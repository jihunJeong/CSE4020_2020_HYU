import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

#For mouse button callback
gLeftButton = False
gRightButton = False

#For scroll callback
gFov = 50.

#For gluPerspective
gWidth = 800
gHeight = 800

#For cursor position callback
gCamwith = -0.
gCamHeight = 0.
gPointX = 0.
gPointY = 0.
gXpos = 0
gYpos = 0

#For toggle Switch
gtoggle = [True, False]

#For Bvh channel Macro
XROTATION = 1
YROTATION = 2
ZROTATION = 3
XPOSITION = 4
YPOSITION = 5
ZPOSITION = 6

#For Bvh Global Variable
gfps = 0.
gframe_cnt = 0
joint_name = []
joint_motion = []
body_stack = []
body_offset = []
start_switch = False
t = 1 		# motion index at t times

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

def drawbody():
	global joint_motion, body_offset, body_stacks, t

	oix = 0		# offset index
	ix = 0		# motion type index

	for i in range(len(body_stack)):
		if body_stack[i] == "{":
			glPushMatrix()
			o1 = np.array(body_offset[0])
			o2 = o1 + np.array(body_offset[oix])

			#Draw the skeleton by line segments
			glBegin(GL_LINES)
			glColor3ub(0,255,255)
			glVertex3fv(o1)
			glVertex3fv(o2)
			glEnd()

			oarr = np.array(body_offset[oix])
			glTranslatef(oarr[0], oarr[1], oarr[2])

			oix += 1

			if body_stack[i+1] == "}":
				continue
			elif i == 0:
				# Root Joint
				#Transition joint
				if int(joint_motion[ix][0]) == 4:
					transX = float(joint_motion[ix][t])
					if int(joint_motion[ix+1][0]) == 5 and int(joint_motion[ix+2][0]) == 6:
						transY = float(joint_motion[ix+1][t])
						transZ = float(joint_motion[ix+2][t])
					else :
						transZ = float(joint_motion[ix+1][t])
						transY = float(joint_motion[ix+2][t])
				elif int(joint_motion[ix][0]) == 5:
					transY = float(joint_motion[ix][t])
					if int(joint_motion[ix+1][0]) == 4 and int(joint_motion[ix+2][0]) == 6:
						transX = float(joint_motion[ix+1][t])
						transZ = float(joint_motion[ix+2][t])
					else :
						transZ = float(joint_motion[ix+1][t])
						transX = float(joint_motion[ix+2][t])
				elif int(joint_motion[ix][0]) == 6:
					transZ = float(joint_motion[ix][t])
					if int(joint_motion[ix+1][0]) == 4 and int(joint_motion[ix+2][0]) == 5:
						transX = float(joint_motion[ix+1][t])
						transY = float(joint_motion[ix+2][t])
					else :
						transY = float(joint_motion[ix+1][t])
						transX = float(joint_motion[ix+2][t])
				glTranslatef(transX, transY, transZ)

				#Rotate joint
				if int(joint_motion[ix+3][0]) == 1:
					if int(joint_motion[ix+4][0]) == 2 and int(joint_motion[ix+5][0]) == 3:
						#XYZ Euler angles
						glRotatef(float(joint_motion[ix+3][t]), 1,0,0)
						glRotatef(float(joint_motion[ix+4][t]), 0,1,0)
						glRotatef(float(joint_motion[ix+5][t]), 0,0,1)
					elif int(joint_motion[ix+4][0]) == 2 and int(joint_motion[ix+5][0]) == 1:
						#XYX Euler angles
						glRotatef(float(joint_motion[ix+3][t]), 1,0,0)
						glRotatef(float(joint_motion[ix+4][t]), 0,1,0)
						glRotatef(float(joint_motion[ix+5][t]), 1,0,0)
					elif int(joint_motion[ix+4][0]) == 3 and int(joint_motion[ix+5][0]) == 2:
						#XZY Euler angles
						glRotatef(float(joint_motion[ix+3][t]), 1,0,0)
						glRotatef(float(joint_motion[ix+4][t]), 0,0,1)
						glRotatef(float(joint_motion[ix+5][t]), 0,1,0)
					elif int(joint_motion[ix+4][0]) == 3 and int(joint_motion[ix+5][0]) == 1:
						#XZX Euler angles
						glRotatef(float(joint_motion[ix+3][t]), 1,0,0)
						glRotatef(float(joint_motion[ix+4][t]), 0,0,1)
						glRotatef(float(joint_motion[ix+5][t]), 1,0,0)
				elif int(joint_motion[ix+3][0]) == 2:
					if int(joint_motion[ix+4][0]) == 3 and int(joint_motion[ix+5][0]) == 1:
						#YZX Euler angles
						glRotatef(float(joint_motion[ix+3][t]), 0,1,0)
						glRotatef(float(joint_motion[ix+4][t]), 0,0,1)
						glRotatef(float(joint_motion[ix+5][t]), 1,0,0)
					elif int(joint_motion[ix+4][0]) == 3 and int(joint_motion[ix+5][0]) == 2:
						#YZY Euler angles
						glRotatef(float(joint_motion[ix+3][t]), 0,1,0)
						glRotatef(float(joint_motion[ix+4][t]), 0,0,1)
						glRotatef(float(joint_motion[ix+5][t]), 0,1,0)
					elif int(joint_motion[ix+4][0]) == 1 and int(joint_motion[ix+5][0]) == 3:
						#YXZ Euler angles
						glRotatef(float(joint_motion[ix+3][t]), 0,1,0)
						glRotatef(float(joint_motion[ix+4][t]), 1,0,0)
						glRotatef(float(joint_motion[ix+5][t]), 0,0,1)
					elif int(joint_motion[ix+4][0]) == 1 and int(joint_motion[ix+5][0]) == 2:
						#YXY Euler angles
						glRotatef(float(joint_motion[ix+3][t]), 0,1,0)
						glRotatef(float(joint_motion[ix+4][t]), 1,0,0)
						glRotatef(float(joint_motion[ix+5][t]), 0,1,0)						
				elif int(joint_motion[ix+3][0]) == 3:
					if int(joint_motion[ix+4][0]) == 1 and int(joint_motion[ix+5][0]) == 2:
						#ZXY Euler angles
						glRotatef(float(joint_motion[ix+3][t]), 0,0,1)
						glRotatef(float(joint_motion[ix+4][t]), 1,0,0)
						glRotatef(float(joint_motion[ix+5][t]), 0,1,0)
					elif int(joint_motion[ix+4][0]) == 1 and int(joint_motion[ix+5][0]) == 3:
						#ZXZ Euler angles
						glRotatef(float(joint_motion[ix+3][t]), 0,0,1)
						glRotatef(float(joint_motion[ix+4][t]), 1,0,0)
						glRotatef(float(joint_motion[ix+5][t]), 0,0,1)
					elif int(joint_motion[ix+4][0]) == 2 and int(joint_motion[ix+5][0]) == 1:
						#ZYX Euler angles
						glRotatef(float(joint_motion[ix+3][t]), 0,0,1)
						glRotatef(float(joint_motion[ix+4][t]), 0,1,0)
						glRotatef(float(joint_motion[ix+5][t]), 1,0,0)
					elif int(joint_motion[ix+4][0]) == 2 and int(joint_motion[ix+5][0]) == 3:
						#ZYZ Euler angles
						glRotatef(float(joint_motion[ix+3][t]), 0,0,1)
						glRotatef(float(joint_motion[ix+4][t]), 0,1,0)
						glRotatef(float(joint_motion[ix+5][t]), 0,0,1)
				ix += 6	
			else :
				#Rotate joint except Root
				if int(joint_motion[ix][0]) == 1:
					if int(joint_motion[ix+1][0]) == 2 and int(joint_motion[ix+2][0]) == 3:
						#XYZ Euler angles
						glRotatef(float(joint_motion[ix][t]), 1,0,0)
						glRotatef(float(joint_motion[ix+1][t]), 0,1,0)
						glRotatef(float(joint_motion[ix+2][t]), 0,0,1)
					elif int(joint_motion[ix+1][0]) == 2 and int(joint_motion[ix+2][0]) == 1:
						#XYX Euler angles
						glRotatef(float(joint_motion[ix][t]), 1,0,0)
						glRotatef(float(joint_motion[ix+1][t]), 0,1,0)
						glRotatef(float(joint_motion[ix+2][t]), 1,0,0)
					elif int(joint_motion[ix+1][0]) == 3 and int(joint_motion[ix+2][0]) == 2:
						#XZY Euler angles
						glRotatef(float(joint_motion[ix][t]), 1,0,0)
						glRotatef(float(joint_motion[ix+1][t]), 0,0,1)
						glRotatef(float(joint_motion[ix+2][t]), 0,1,0)
					elif int(joint_motion[ix+1][0]) == 3 and int(joint_motion[ix+2][0]) == 1:
						#XZX Euler angles
						glRotatef(float(joint_motion[ix][t]), 1,0,0)
						glRotatef(float(joint_motion[ix+1][t]), 0,0,1)
						glRotatef(float(joint_motion[ix+2][t]), 1,0,0)
				elif int(joint_motion[ix][0]) == 2:
					if int(joint_motion[ix+1][0]) == 3 and int(joint_motion[ix+2][0]) == 1:
						#YZX Euler angles
						glRotatef(float(joint_motion[ix][t]), 0,1,0)
						glRotatef(float(joint_motion[ix+1][t]), 0,0,1)
						glRotatef(float(joint_motion[ix+2][t]), 1,0,0)
					elif int(joint_motion[ix+1][0]) == 3 and int(joint_motion[ix+2][0]) == 2:
						#YZY Euler angles
						glRotatef(float(joint_motion[ix][t]), 0,1,0)
						glRotatef(float(joint_motion[ix+1][t]), 0,0,1)
						glRotatef(float(joint_motion[ix+2][t]), 0,1,0)
					elif int(joint_motion[ix+1][0]) == 1 and int(joint_motion[ix+2][0]) == 3:
						#YXZ Euler angles
						glRotatef(float(joint_motion[ix][t]), 0,1,0)
						glRotatef(float(joint_motion[ix+1][t]), 1,0,0)
						glRotatef(float(joint_motion[ix+2][t]), 0,0,1)
					elif int(joint_motion[ix+1][0]) == 1 and int(joint_motion[ix+2][0]) == 2:
						#YXY Euler angles
						glRotatef(float(joint_motion[ix][t]), 0,1,0)
						glRotatef(float(joint_motion[ix+1][t]), 1,0,0)
						glRotatef(float(joint_motion[ix+2][t]), 0,1,0)						
				elif int(joint_motion[ix][0]) == 3:
					if int(joint_motion[ix+1][0]) == 1 and int(joint_motion[ix+2][0]) == 2:
						#ZXY Euler angles
						glRotatef(float(joint_motion[ix][t]), 0,0,1)
						glRotatef(float(joint_motion[ix+1][t]), 1,0,0)
						glRotatef(float(joint_motion[ix+2][t]), 0,1,0)
					elif int(joint_motion[ix+1][0]) == 1 and int(joint_motion[ix+2][0]) == 3:
						#ZXZ Euler angles
						glRotatef(float(joint_motion[ix][t]), 0,0,1)
						glRotatef(float(joint_motion[ix+1][t]), 1,0,0)
						glRotatef(float(joint_motion[ix+2][t]), 0,0,1)
					elif int(joint_motion[ix+1][0]) == 2 and int(joint_motion[ix+2][0]) == 1:
						#ZYX Euler angles
						glRotatef(float(joint_motion[ix][t]), 0,0,1)
						glRotatef(float(joint_motion[ix+1][t]), 0,1,0)
						glRotatef(float(joint_motion[ix+2][t]), 1,0,0)
					elif int(joint_motion[ix+1][0]) == 2 and int(joint_motion[ix+2][0]) == 3:
						#ZYZ Euler angles
						glRotatef(float(joint_motion[ix][t]), 0,0,1)
						glRotatef(float(joint_motion[ix+1][t]), 0,1,0)
						glRotatef(float(joint_motion[ix+2][t]), 0,0,1)
				ix += 3
		elif body_stack[i] == "}":
			glPopMatrix()
	if start_switch == False:
		t += 0
	else :
		t += 1
	if t == (int(gframe_cnt)-1):
		t = 2

def render():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glLoadIdentity()
    gluLookAt(0, 0, 8, 0,0,0, 0,.1,0)
   
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(gFov, gWidth/gHeight, 5, 1000)
    glTranslatef(0., 0., -800)
    #glRotatef(45, 1, 0, 0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glTranslatef(gPointX, 0, 0)
    glTranslatef(0, gPointY, 0)
    glRotatef(gCamHeight, 1, 0, 0)
    glRotatef(gCamwith, 0, 1, 0)
 
    drawFrame()
    drawGrid()

    glEnable(GL_NORMALIZE)  # try to uncomment: lighting will be incorrect if you scale the object
    # glEnable(GL_RESCALE_NORMAL)
    glColor3ub(255, 255, 255)
    
    drawbody()

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
    gFov -= yoffset

def key_callback(window, key, scancode, action, mods):
	global gtoggle, continue_switch, start_switch

	if action==glfw.PRESS or action==glfw.REPEAT:
		if key == glfw.KEY_Z:
			#Set toggle switch for glPolygon
			gtoggle[0] = not gtoggle[0]
		elif key == glfw.KEY_SPACE:
			start_switch = not start_switch
def hierarchy(input_list):
	global XPOSTION, YPOSTION, ZPOSTION, ZROTATION, XROTATION, YROTATION

	if input_list[0] == "ROOT" or input_list[0] == "JOINT":
		joint_name.append(input_list[1])
	elif input_list[0] == "{" or input_list[0] == "}":
		body_stack.append(input_list[0])
	elif input_list[0] == "OFFSET":
		offset_xyz = (float(input_list[1]), float(input_list[2]), float(input_list[3]))
		body_offset.append(offset_xyz)
	elif input_list[0] == "CHANNELS":
		#Check Channel count and iterate the joint
		for i in range(2, int(input_list[1])+2):
			joint_motion.append([])
			index = len(joint_motion) - 1
			if input_list[i].upper() == "XPOSITION":
				joint_motion[index].append(XPOSITION)
				joint_motion[index].append(0.0)
			elif input_list[i].upper() == "YPOSITION":
				joint_motion[index].append(YPOSITION)
				joint_motion[index].append(0.0)
			elif input_list[i].upper() == "ZPOSITION":
				joint_motion[index].append(ZPOSITION)
				joint_motion[index].append(0.0)
			elif input_list[i].upper() == "XROTATION":
				joint_motion[index].append(XROTATION)
				joint_motion[index].append(0.0)
			elif input_list[i].upper() == "YROTATION":
				joint_motion[index].append(YROTATION)
				joint_motion[index].append(0.0)
			elif input_list[i].upper() == "ZROTATION":
				joint_motion[index].append(ZROTATION)
				joint_motion[index].append(0.0)

def motion(input_list):
	global gfps, gframe_cnt

	if input_list[0] == "Frames:":
		gframe_cnt = input_list[1]
	elif input_list[0] == "Frame":
		gfps = 1.0 / float(input_list[2])
	else :
		for i in range(len(joint_motion)):
			joint_motion[i].append(input_list[i])


def drop_callback(window, paths):
	global joint_name, joint_motion, body_stack, body_offset
	global gfps, gframe_cnt, continue_switch, start_switch, t

	gfps = 0.
	gframe_cnt = 0
	continue_switch = True
	start_switch = False
	t = 1 		# motion index at t times
	joint_name = []
	joint_motion = []
	body_stack = []
	body_offset = []

	condtion = "HIERARCHY"

	#Get paths to read Bvh files and fild name
	paths = str(paths)
	file_name = list(paths.split('/'))[-1][:-2]
	
	#Open Bvh file
	f = open(paths[2:-2], 'r')

	while True:
		line = f.readline()
		if not line:
			break;

		input_list = list(line.split())
		
		#check hierarcy or motion
		if input_list[0] == "MOTION":
			condtion = "MOTION"
			continue

		if condtion == "HIERARCHY":
			hierarchy(input_list)
		elif condtion == "MOTION":
			motion(input_list)
	

	#Print out the information to stdout(console)
	print(" ")
	print("==============================================")
	print("File name : " + file_name)
	print("Number of frames : " + str(gframe_cnt))
	print("FPS (which is 1/FrameTime : " + str(round(gfps, 3)))
	print("Number of joints (including root) : " + str(len(joint_name)))
	print("List of all joint names : " + joint_name[0])
	for i in range(1, len(joint_name)):
		print("                          " + joint_name[i])
	print("==============================================")

def size_callback(window, width, height):
    global gWidth, gHeight
    gWidth = width
    gHeight = height
    glViewport(0, 0, gWidth, gHeight)

def main():
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
    glfw.set_drop_callback(window, drop_callback)

    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
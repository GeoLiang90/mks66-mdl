import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'
    polygons=[]
    edges=[]
    #print symbols
    '''
    for symbol in symbols:
        print symbol
    '''
    constants=[]
    for command in commands:
        print command
        if command['op'] == 'constants':
            constants.append(command['constants'])
        elif command['op'] == 'sphere':
            #print 'SPHERE\t' + str(args)
            add_sphere(polygons,
                       float(command['args'][0]), float(command['args'][1]), float(command['args'][2]),
                       float(command['args'][3]), step_3d)
            matrix_mult( stack[-1], polygons )
            if (command['constants'] != None) and (command['constants'] in constants):
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, command['constants'])
            else:
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, reflect)
            polygons = []

        elif command['op'] == 'torus':
            #print 'TORUS\t' + str(args)
            add_torus(polygons,
                      float(command['args'][0]), float(command['args'][1]), float(command['args'][2]),
                      float(command['args'][3]), float(command['args'][4]), step_3d)
            matrix_mult( stack[-1], polygons )
            if (command['constants'] != None) and (command['constants'] in constants):
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, command['constants'])
            else:
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, reflect)
            polygons = []

        elif command['op'] == 'box':
            #print 'BOX\t' + str(args)
            add_box(polygons,
                    float(command['args'][0]), float(command['args'][1]), float(command['args'][2]),
                    float(command['args'][3]), float(command['args'][4]), float(command['args'][5]))
            matrix_mult( stack[-1], polygons )
            if (command['constants'] != None) and (command['constants'] in constants):
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, command['constants'])
            else:
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, reflect)
            polygons = []
            
        elif command['op'] == 'line':
            #print 'LINE\t' + str(args)

            add_edge( edges,
                      float(command['args'][0]), float(command['args'][1]), float(command['args'][2]),
                      float(command['args'][3]), float(command['args'][4]), float(command['args'][5]) )
            matrix_mult( stack[-1], edges )
            draw_lines(edges, screen, zbuffer, color)
            edges = []

        elif command['op'] == 'scale':
            #print 'SCALE\t' + str(args)
            t = make_scale(float(command['args'][0]), float(command['args'][1]), float(command['args'][2]))
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]

        elif command['op'] == 'move':
            #print 'MOVE\t' + str(args)
            t = make_translate(float(command['args'][0]), float(command['args'][1]), float(command['args'][2]))
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]

        elif command['op'] == 'rotate':
            #print 'ROTATE\t' + str(args)
            theta = float(command['args'][1]) * (math.pi / 180)
            if command['args'][0] == 'x':
                t = make_rotX(theta)
            elif command['args'][0] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]

        elif command['op'] == 'push':
            stack.append( [x[:] for x in stack[-1]] )

        elif command['op'] == 'pop':
            stack.pop()

        elif command['op'] == 'display' or command['op'] == 'save':
            if command['op'] == 'display':
                display(screen)
            else:
                save_extension(screen, command['args'][0] + ".png")

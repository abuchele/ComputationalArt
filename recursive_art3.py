""" This is my computational art project!
    Anna Buchele """

import random
from PIL import Image
import math



def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    if min_depth < 1:
        if max_depth < 1:
            depth = 0
        else:
            depth=random.randint(0,max_depth)
    else:
        depth=random.randint(min_depth,max_depth)  
    exists = 'functout' in locals() or 'functout' in globals()
    if exists == False:
        functout =[]
    if depth > 0:
        
        r= random.randint(0,9)
        a= random.randint(0,2)
        b= random.randint(0,2)
        k= random.randint(1,20)
        if a == 0:
            m = "x"
        elif a == 1:
            m = "y"
        elif a == 2:
            m = "old"
        else:
            m = "pre"
        if b == 0:
            n = "x"
        elif b == 1:
            n = "y"
        elif b == 2:
            n = "old"
        else:
            n = "pre"        
        if r == 0:
            functin= ["prod", m, n]
        elif r == 1:
            functin= ["avg", m, n]
        elif r == 2:
            functin= ["cos_pi", m, k] 
        elif r == 3:
            functin= ["sin_pi", m, k]
        elif r == 4:
            functin= ["pwr", m,k]
        elif r == 5: 
            functin= ["self", m]
        elif r == 6:
            functin= ["atan", m, k]
        elif r == 7:
            functin= ["arcsin", m, k]
        elif r == 8:
            functin= ["cbe", m, k]
        elif r == 9:
            functin= ["1minus", m]

        funct = build_random_function(min_depth-1, max_depth-1) 
        if funct == None:
            functout+= [functin]
        else:
            functout+=[functin]
            for a in range (len(funct)):
                r = funct[a]
                functout+= [r]
        return functout








def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
    """
    bringitback = []
    ans = 0
    pre = x*y
    for a in range (len(f)):
        x = float(x)
        y = float(y)
        count = 0
        fu = f[a]
        #fu = fa[0]
        # print fu
        fun = fu[0]

        if len(fu) > 1:
            if fu[1] == "x":
                m = x
            elif fu[1] == "y":
                m = y
            elif fu[1] == "pre":
                m = pre
            elif fu[1] == "old":
                if len(bringitback) >0:
                    m = bringitback[0]
                    del bringitback[0]
                else:
                    m = pre
            if len(fu) > 2:
                if fu[2] == "x":
                    n = x
                elif fu[2] == "y":
                    n = y
                elif fu[2] == "pre":
                    n = pre
                elif type(fu[2]) == int:
                    k = fu[2]
                else:
                    if len(bringitback) > 0:
                        m = bringitback[0]
                        del bringitback[0]
                    else:
                        m = pre
        if a == 0:
            m = float(x)
            n = float(y)
        if fun == 'prod': 
            ans= (m * n)
        elif fun == 'avg':
            ans= (m + n)/2
        elif fun == "cos_pi":
            ans= math.cos(k*math.pi*m)
        elif fun == "sin_pi":
            ans= math.sin(k*math.pi*m)
        elif fun == "atan": 
            ans= math.atan(k*math.pi*m)/math.pi
        elif fun == "cbe":
            ans= abs(m)**(2)
            ans = math.copysign(ans,m)
        elif fun == "pwr": 
            ans= abs(m)**(k)
        elif fun == "self":
            ans = m
        elif fun == "arcsin": 
            ans =  math.asin(m)/(math.pi/2)
        elif fun == "1minus": 
            ans = 1-abs(m)
            ans = math.copysign(ans,m)
        else:
            print '!!'
        if m is not pre and n is not pre:
            if a is not 0:
                bringitback.append(pre)
        pre = ans


    if len(bringitback) > 0:
        for a in range (len(bringitback)-1):
            if a % 2 ==0:
                ans = ans * bringitback[a]


    return ans



def remap_interval(val,input_interval_start,input_interval_end,output_interval_start,output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
        >>> remap_interval(0.032, -1, 1, 0, 255)
        131.58
    """
    inputinterval= float(input_interval_end) - float(input_interval_start)
    outputinterval= float(output_interval_end) - float(output_interval_start)
    valremap= float(((outputinterval)*(val-input_interval_start)) / (inputinterval)) +float(output_interval_start)
    return valremap


def color_map(val,minv=-1,maxv=1):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0, -1, 1)
        0
        >>> color_map(1.0, -1, 1)
        255
        >>> color_map(0.0, -1, 1)
        127
        >>> color_map(0.5, -1, 1)
        191
    """
    color_code = int(remap_interval(val, minv, maxv, 0, 255))
    return (color_code)

def color_map2(val,minv=-1,maxv=1):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0, -1, 1)
        0
        >>> color_map(1.0, -1, 1)
        255
        >>> color_map(0.0, -1, 1)
        127
        >>> color_map(0.5, -1, 1)
        191
    """
    inputinterval= minv - maxv
    output_interval_start = 0
    output_interval_end = float(255)
    outputinterval= output_interval_end - output_interval_start
    valremap= (((outputinterval)*(val-minv)) / (inputinterval)) +(output_interval_start)
    color_code= int(valremap)
    return (color_code)



def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # creating functions for red, green, and blue channels
    red_function = build_random_function(6,9)
    green_function = build_random_function(3, 9)
    blue_function = build_random_function(7, 9)


    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixelsred= []
    pixelsblue= []
    pixelsgreen= []
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
    #         pixelsred += [evaluate_random_function(red_function, x, y)]
    # minred= min(pixelsred)
    # # print minred
    # maxred= max(pixelsred)
    # # if minred * maxred <0.00005:
    # #     print 'nope'
    # #else:
    # # print maxred
    # for i in range(x_size):
    #     for j in range(y_size):
    #         pixels[i,j] = (color_map2(evaluate_random_function(red_function, x, y), minred, maxred), 0, 0)


            # pixels[i,j] = color_map(evaluate_random_function([["1minus","x",'y']],x,y))
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)), 
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y)))

        im.save(filename)


generate_art("myart26.png")


"""Testing functions"""
# def testing(runs):
#   for n in range (runs):
#       r = random.uniform(-1,1)
#       s = random.uniform(-1,1)
#       for a in range (50):
#           k = build_random_function(10,15)
#           j = evaluate_random_function(k, r, s)
#           if -1 > j > 1:
#               print k
#               return "NOPE"
#       if -1 > j > 1:
#           print k
#           return "NOPE"
#   return "OK"

# print testing(400)

# f = [['cos_pi', 'pre'], [['sqrt', 'x'], [['cos_pi', 'x'], [['sqrt', 'x'], [['cubrt', 'y'], [['1_minus', 'y'], [['sqr', 'pre'], [['avg', 'y', 'pre']]]]]]]]]
# for i in range (250):
#   for j in range (250):
#       x = remap_interval(i, 0, 250, -1, 1)
#         y = remap_interval(j, 0, 250, -1, 1)
#         e = evaluate_random_function(f,x,y)
#         if e > 1:
#           print f
#           print e
#           print x
#           print y
#           print '[ERROR]'
#         if e < -1:
#           print e
#           print f 
#           print x
#           print y
#           print '[NEGERROR]'

# if __name__ == '__main__':
#     import doctest
#     doctest.testmod()

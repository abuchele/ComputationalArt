""" 
    Anna Buchele

    This is my computational art project revision for Mini Project 5. 
    The original program took ~31 seconds to run, so for MP5 I profiled it 
    and made it a lot faster. As a side effect, the art looks better since
    I had to rewrite a lot of it and fixed some bugs while doing that. 
    It takes ~2 seconds to run now!

    """

import random
from PIL import Image
import math

def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth.

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    #calculating the depth

    if min_depth < 1:
        if max_depth < 1:
            depth = 0
        else:
            depth=random.randint(0,max_depth)
    elif min_depth == max_depth:
        depth = min_depth
    else:
        depth=random.randint(min_depth,max_depth)  
    functout =[]

    #full recursive proved to be problematic, so rewrote as for-loop
    for n in range (depth):
        
        # rolling for random vals seperately, so if the r-value 
        # means we don't need a k or m value, we don't waste
        # time getting it

        r= random.randint(0,9)

        if r == 0: 
            functin= ["y"]
        if r == 1:
            functin= ["x"]
        elif r == 2:
            functin= ["1minus"]
        elif r == 3:
            functin= ["arcsin"]
        else:
            if r < 8:
                k= random.randint(1,20)
                if r == 4:
                    functin= ["cos_pi",k] 
                elif r == 5:
                    functin= ["sin_pi", k]
                elif r == 6:
                    functin= ["pwr", k]
                elif r == 7:
                    functin= ["atan", k]

            else:
                m = build_random_function(1,1)
                if r == 8:
                    functin= ["prod", m]
                elif r == 9:
                    functin= ["avg", m]

            functout+= [functin]

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
    ans = 0
    pre = x * y
    for f_piece in f:
        # if f_piece is only one item long:
        if f_piece == "x":
            ans = x 
        elif f_piece == "y":
            ans =  y 
        elif f_piece == "1minus":
            ans = 1-abs(pre)
        else:
            # if f_piece is longer than one item:
            # these are the only functions that could be longer
            # than one item that don't require k 
            part = f_piece[0]
            if part == "x":
                ans = x * pre
            elif part == "y":
                ans = y * pre
            elif part == "arcsin": 
                ans =  math.asin(pre)/(math.pi/2)
            else:
                # k is 2nd val, either fn or integer. if fn is 'prod'
                # or 'avg', k must be fn. Otherwise, k is integer.
                k = f_piece[1]
                if part == 'prod': 
                    ans= (evaluate_random_function(k,x,y))*(pre)
                elif part == 'avg':
                    ans= ((evaluate_random_function(k,x,y))+pre)*0.5
                elif part == "cos_pi":
                    ans= math.cos(math.pi*pre*k)
                elif part == "sin_pi":
                    ans= math.sin(math.pi*pre*k)
                elif part == "pwr": 
                    ans= pre**(k)
                elif part == "atan": 
                    ans= math.atan(k*math.pi*pre)/math.pi
            pre = ans
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
    inputinterval= (input_interval_end) - (input_interval_start)
    outputinterval= float(output_interval_end) - float(output_interval_start)
    valremap= float(((outputinterval)*float(val-input_interval_start)) / (inputinterval)) +float(output_interval_start)
    return valremap


def color_map(val):
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
    color_code = int(remap_interval(val, -1, 1, 0, 255))
    return (color_code)

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
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)), 
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y)))

    im.save(filename)


generate_art("myart41.png")



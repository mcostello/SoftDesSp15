"""
Created on Sun Feb 14  11:24:42 2015

@author: Michael Costello

"""
import random
import math
from PIL import Image

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

    return add_func(max_depth)

    # prod(a,b) = a*b
    # avg(a,b) = 0.5*(a+b)
    # cos_pi(a) = cos(pi*a)
    # sin_pi(a) = sin(pi*a)
    # x(a,b) = a
    # y(a,b) = b

    # return ["sin_pi"]
def add_func(recurse):
    if recurse == 1:
        return random.choice(["x","y"])
    func_list = [
        ["prod",add_func(recurse-1),add_func(recurse-1)],
        ["avg",add_func(recurse-1),add_func(recurse-1)],
        ["cos_pi",add_func(recurse-1)],
        ["sin_pi",add_func(recurse-1)],
        ["x",add_func(recurse-1)],
        # ["eul_ovr_eul",add_func(recurse-1)],
        # ["half",add_func(recurse-1)],
        ["tenpi",add_func(recurse-1)],
        ["sincos",add_func(recurse-1)],
        ["hypotenuse",add_func(recurse-1),add_func(recurse-1)]
        ]
    return random.choice(func_list)


def evaluate_random_function(f,x,y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        f[0] is the fn, f[1] is the argument, f[2] is the optional second argument
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
    """
    if f[0] == "x":
        return x
    elif f[0] =="y":
        return y
    elif f[0] == "prod":
        return evaluate_random_function(f[1], x, y)*evaluate_random_function(f[2], x, y)
    elif f[0] == "avg":
        return (evaluate_random_function(f[1], x, y)+evaluate_random_function(f[2], x, y))/2.0
    elif f[0] == "cos_pi":
        return math.cos(math.pi*evaluate_random_function(f[1], x, y))
    elif f[0] == "sin_pi":
        return math.sin(math.pi*evaluate_random_function(f[1], x, y))
    # elif f[0] == "eul_ovr_eul":
    #     return (2.719**evaluate_random_function(f[1], x, y))/-2.719
    # elif f[0] == "half":
    #     return 0.5 * evaluate_random_function(f[1], x, y)
    elif f[0] == "tenpi":
        return math.sin(10*math.pi * evaluate_random_function(f[1], x, y))
    elif f[0] == "sincos":
        return math.sin(.3*math.pi * evaluate_random_function(f[1], x, y))*math.cos(.3*math.pi * evaluate_random_function(f[1], x, y))
    elif f[0] == "hypotenuse":
        return math.sqrt((evaluate_random_function(f[1], x, y))**2 +(evaluate_random_function(f[1], x, y))**2)


def remap_interval(val, input_interval_start, input_interval_end, output_interval_start, output_interval_end):
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
    """
    fraction_difference = 1.0* (val - input_interval_start) / (input_interval_end - input_interval_start)
    return fraction_difference * (output_interval_end - output_interval_start) + output_interval_start


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


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
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7, 9)
    green_function = build_random_function(7, 9)
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
                    color_map(evaluate_random_function(blue_function, x, y))
                    )
    im.save(filename)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    generate_art("myart_19.png")
    #add_func(2)
    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    # test_image("noise.png")

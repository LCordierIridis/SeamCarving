from math import pow

RED = 0
GREEN = 1
BLUE = 2

MAX_ENERGY = 390150 # 255² * 6
MAX_COLOR_VALUE = 255

def convolution(image_pixels, orig_image_width, orig_image_height, col, row):

    # Border special cases
    previous_col = col - 1 
    if previous_col < 0: 
        previous_col = orig_image_width - 1

    next_col = col + 1 
    if next_col >= orig_image_width:
        next_col = 0

    previous_row = row - 1
    if previous_row < 0:
        previous_row = orig_image_height - 1

    next_row = row + 1
    if next_row >= orig_image_height:
        next_row = 0
        
    # print("Pixel {}:{} ----- next X : {}:{} ----- next Y : {}:{}".format(col, row, previous_col, next_col, previous_row, next_row))

    # Calculate horizontal color differences
    delta_Rx = image_pixels[next_col, row][RED] - image_pixels[previous_col, row][RED]
    delta_Gx = image_pixels[next_col, row][GREEN] - image_pixels[previous_col, row][GREEN]
    delta_Bx = image_pixels[next_col, row][BLUE] - image_pixels[previous_col, row][BLUE]

    squared_delta_x = pow(delta_Rx, 2) + pow(delta_Gx, 2) + pow(delta_Bx, 2)

    # Calculate vertical color differences
    delta_Ry = image_pixels[col, next_row][RED] - image_pixels[col, previous_row][RED]
    delta_Gy = image_pixels[col, next_row][GREEN] - image_pixels[col, previous_row][GREEN]
    delta_By = image_pixels[col, next_row][BLUE] - image_pixels[col, previous_row][BLUE]

    squared_delta_y = pow(delta_Ry, 2) + pow(delta_Gy, 2) + pow(delta_By, 2)

    return squared_delta_x + squared_delta_y

def scale_energy(value):
    return int(value * MAX_COLOR_VALUE / MAX_ENERGY)

def get_energy_image(image):
    image_pixels = image.load()
    orig_image_width, orig_image_height = image.size

    image_energy = []

    for col in range(0, orig_image_width):
        image_energy.append([])

        for row in range(0, orig_image_height):
            pixel_energy = convolution(image_pixels, orig_image_width, orig_image_height, col, row)
            image_energy[col].append(pixel_energy)
            
            pixel_energy = scale_energy(pixel_energy)
            image_pixels[col, row] = (pixel_energy, pixel_energy, pixel_energy)

    image.save('Images/energy_cat.png')
    return image_energy
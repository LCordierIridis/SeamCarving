import sys
import numpy
from PIL import Image
import ImageProcessing as ip

from Seam import Seam, SeamType
from CustomImage import CustomImage

orig_image_width = 0 
orig_image_height = 0

# we reverse row and col compared to image to facilitate row by row processing
def initGeneralTermsTable():
    generalTermsTable = []

    for row in range(0, orig_image_height):
        generalTermsTable.append([])
        for col in range(0, orig_image_width):
            generalTermsTable[row].append(0)

    return generalTermsTable

def getGeneralTermsTable(image_energy):
    generalTermsTable = initGeneralTermsTable()

    # For each pixel
    for row in range(0, orig_image_height):
        for col in range(0, orig_image_width):
            # We store the energy value in same location in both arrays
            generalTermsTable[row][col] = int(image_energy[col][row])

            # We then add the highest value from the previous row
            # Only from neighbours and only from row 1 and up
            if(row != 0):
                min = generalTermsTable[row - 1][col]

                if(col != 0):
                    if(generalTermsTable[row - 1][col - 1] < min):
                        min = generalTermsTable[row - 1][col - 1]

                if(col != orig_image_width - 1):
                    if(generalTermsTable[row - 1][col + 1] < min):
                        min = generalTermsTable[row - 1][col + 1]

                generalTermsTable[row][col] += min

    # for row in range(0, orig_image_height):
    #     print("{} {} {}".format(generalTermsTable[row][0], generalTermsTable[row][1], generalTermsTable[row][2]))
    #     print("{} {} {}".format(image_energy[0][row], image_energy[1][row], image_energy[2][row]))
    #     print("\n")

    return generalTermsTable

def findSeam(generalTermsTable):
    seam = Seam(SeamType.V, orig_image_height)

    # We are looking for the minimum, so we inverse the table to start from the top
    # Where the totals of each path are
    for row in range(orig_image_height - 1, -1, -1):
        # print(row)

        # When on the first row we look for the smallest value
        if(row == orig_image_height - 1):
            min = sys.maxsize

            for col in range(0, orig_image_width):
                if(generalTermsTable[row][col] < min):
                    min = generalTermsTable[row][col]
                    seam.pixels[row] = col

        else :
            previous_optimal_col = seam.pixels[row + 1]

            # We use previous_optimal_col + 2 as the outer bound because range() excludes
            # the outer bound
            pixels_below = range(previous_optimal_col - 1, previous_optimal_col + 2)

            if(previous_optimal_col == 0):
                pixels_below = range(previous_optimal_col, previous_optimal_col + 2)

            if(previous_optimal_col == orig_image_width - 1):
                pixels_below = range(previous_optimal_col - 1, previous_optimal_col + 1)

            # We then look for the minimal value from these
            min = sys.maxsize

            for col in pixels_below:
                if(generalTermsTable[row][col] < min):
                    min = generalTermsTable[row][col]
                    seam.pixels[row] = col

    print(seam.pixels)

    return seam

def deleteSeam(seam, image):
    image_array = numpy.array(image)

    for row, col in enumerate(seam.pixels):
        image_array = numpy.delete(image_array, row * orig_image_width + col)

    image = Image.fromarray(image_array)
    return image

def drawSeam(seam, image):
    image_pixels = image.load()

    print("Seam : ")
    for row, col in enumerate(seam.pixels):
            print("{}:{}".format(col, row))
            image_pixels[col, row] = (255, 0, 0)

    image.save('Images/seam_cat.png')

image = Image.open('Images/cat.png')
customImage = CustomImage(image)
customImage.reduceByPercent(0.01)
# image_pixels = image.load()

# orig_image_width, orig_image_height = image.size

# image_energy = ip.get_energy_image(image)
# generalTermsTable = getGeneralTermsTable(image_energy)
# seam = findSeam(generalTermsTable)
# drawSeam(seam, image)
# image = deleteSeam(seam, image)
# image.save('Images/carved_cat.png')

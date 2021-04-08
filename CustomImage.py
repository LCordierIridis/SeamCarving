import sys
from typing import Tuple
import numpy

import ImageProcessing as ip

from imageio import imread, imwrite
from PIL import Image
from Seam import Seam, SeamType

class CustomImage:
    image_file = None

    image = []
    energy_image = []
    generalTermsTable = []

    height = 0
    width = 0

    H_seams_left = 0
    V_seams_left = 0


    def __init__(self, filename):
        self.image_file = Image.open(filename)
        self.image = self.image_file.load()
        self.image = numpy.array(self.image_file)
        
        self.width, self.height = self.image_file.size


    def reduceByPercent(self, resize_percentage):
        self.H_seams_left = int(self.width * resize_percentage)
        self.V_seams_left = int(self.height * resize_percentage)

        print("We need to remove {} horizontal seams and {} vertical seams to achieve a {}% reduction in image size".format(self.H_seams_left, self.V_seams_left, resize_percentage*100))

        # TODO : implement algorithm to determine if it's better to remove horizontal or vertical seam first
        while(self.H_seams_left > 0 and self.V_seams_left > 0):
            self.removeHorizontalSeam()
            self.H_seams_left -= 1
            print("{} Horizontal seams to remove".format(self.H_seams_left))

            self.removeVerticalSeam()
            self.V_seams_left -= 1
            print("{} Vertical seams to remove".format(self.V_seams_left))

        while(self.H_seams_left > 0):
            self.removeHorizontalSeam()
            self.H_seams_left -= 1
            print("{} Horizontal seams to remove".format(self.H_seams_left))

        while(self.V_seams_left > 0):
            self.removeVerticalSeam()
            self.V_seams_left -= 1
            print("{} Vertical seams to remove".format(self.V_seams_left))

        imwrite("Images/Cat_Cropped_{}.png".format(int(resize_percentage * 100)), self.image)


    def PrepareSeamRemoval(self):
        self.calculateEnergyImage()
        self.calculateGeneralTermsTable()


    def removeFoundSeam(self, seam):
        mask = numpy.ones((self.height, self.width), dtype=numpy.bool)

        for row, col in enumerate(seam.pixels):
            mask[row, col] = False

        mask = numpy.stack([mask] * 3, axis=2)

        self.image = self.image[mask].reshape(self.height, self.width - 1, 3)
        self.width -= 1


    def removeHorizontalSeam(self):
        self.PrepareSeamRemoval()
        seam = self.findHorizontalSeam()

        self.removeFoundSeam(seam)


    def inverseHeightAndWidth(self):
        tmp = self.width
        self.width = self.height
        self.height = tmp


    def removeVerticalSeam(self):
        self.image = numpy.rot90(self.image, 1, (0, 1))

        self.inverseHeightAndWidth()
        self.removeHorizontalSeam()
        self.inverseHeightAndWidth()
        
        self.image = numpy.rot90(self.image, 3, (0, 1))


    def calculateEnergyImage(self):
        # self.image = self.image_file.load()

        self.energy_image = []

        for col in range(0, self.width):
            self.energy_image.append([])

            for row in range(0, self.height):
                pixel_energy = ip.convolution(self.image, self.width, self.height, col, row)
                self.energy_image[col].append(pixel_energy)


    def calculateGeneralTermsTable(self):
        self.initGeneralTermsTable()

        # For each pixel
        for row in range(0, self.height):
            for col in range(0, self.width):
                # We store the energy value in same location in both arrays
                self.generalTermsTable[row][col] = int(self.energy_image[col][row])

                # We then add the highest value from the previous row
                # Only from neighbours and only from row 1 and up
                if(row != 0):
                    min = self.generalTermsTable[row - 1][col]

                    if(col != 0):
                        if(self.generalTermsTable[row - 1][col - 1] < min):
                            min = self.generalTermsTable[row - 1][col - 1]

                    if(col != self.width - 1):
                        if(self.generalTermsTable[row - 1][col + 1] < min):
                            min = self.generalTermsTable[row - 1][col + 1]

                    self.generalTermsTable[row][col] += min

        # for row in range(0, orig_image_height):
        #     print("{} {} {}".format(generalTermsTable[row][0], generalTermsTable[row][1], generalTermsTable[row][2]))
        #     print("{} {} {}".format(image_energy[0][row], image_energy[1][row], image_energy[2][row]))
        #     print("\n")


    def initGeneralTermsTable(self):
        self.generalTermsTable = []

        for row in range(0, self.height):
            self.generalTermsTable.append([])
            for col in range(0, self.width):
                self.generalTermsTable[row].append(0)


    def findHorizontalSeam(self):
        seam = None
        seam = Seam(SeamType.H, self.height)

        # We are looking for the minimum, so we inverse the table to start from the top
        # Where the totals of each path are
        for row in range(self.height - 1, -1, -1):
            # print(row)

            # When on the first row we look for the smallest value
            if(row == self.height - 1):
                min = sys.maxsize

                for col in range(0, self.width):
                    if(self.generalTermsTable[row][col] < min):
                        min = self.generalTermsTable[row][col]
                        seam.pixels[row] = col

            else :
                previous_optimal_col = seam.pixels[row + 1]

                # We use previous_optimal_col + 2 as the outer bound because range() excludes
                # the outer bound
                pixels_below = range(previous_optimal_col - 1, previous_optimal_col + 2)

                if(previous_optimal_col == 0):
                    pixels_below = range(previous_optimal_col, previous_optimal_col + 2)

                if(previous_optimal_col == self.width - 1):
                    pixels_below = range(previous_optimal_col - 1, previous_optimal_col + 1)

                # We then look for the minimal value from these
                min = sys.maxsize

                for col in pixels_below:
                    if(self.generalTermsTable[row][col] < min):
                        min = self.generalTermsTable[row][col]
                        seam.pixels[row] = col

        # print("Horizontal seam found : {}\n".format(seam.pixels))

        return seam


# ------------------------------------------------------------ GETTERS & SETTERS ------------------------------------------------------------

    def getEnergyImage(self):
        return self.energy_image 
from PIL import Image
import ImageProcessing as ip

orig_image_width = 0 
orig_image_height = 0

def initGeneralTermsTable():
    generalTermsTable = []

    for col in range(0, orig_image_width):
        generalTermsTable.append([])
        for row in range(0, orig_image_height):
            generalTermsTable[col].append(0)

    return generalTermsTable

def getGeneralTermsTable(image_energy):
    generalTermsTable = initGeneralTermsTable()

    for row in range(0, orig_image_height):
        for col in range(0, orig_image_width):
            generalTermsTable[col][row] = int(image_energy[col][row])

            if(row != 0):
                max = generalTermsTable[col][row - 1]

                if(col != 0):
                    if(generalTermsTable[col - 1][row - 1] > max):
                        max = generalTermsTable[col - 1][row - 1]

                if(col != orig_image_width - 1):
                    if(generalTermsTable[col + 1][row - 1] > max):
                        max = generalTermsTable[col + 1][row - 1]

                generalTermsTable[col][row] += max

image = Image.open('Images/cat.png')

orig_image_width, orig_image_height = image.size

image_energy = ip.get_energy_image(image)
getGeneralTermsTable(image_energy)
from PIL import Image
import ImageProcessing as ip

image = Image.open('Images/cat.png')
image_energy = ip.get_energy_image(image)
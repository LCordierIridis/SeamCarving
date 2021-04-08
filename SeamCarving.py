from PIL import Image
from CustomImage import CustomImage

import sys

def main():
    if(len(sys.argv) != 4):
        print("Use as follows : 'py SeamCarving.py cat.png 50 10'")

    print("{} {} {}".format(sys.argv[1], sys.argv[2], sys.argv[3]))

    imagepath = 'Images/{}'.format(sys.argv[1])
    customImage = CustomImage(imagepath)

    h_percent = float(sys.argv[2])
    v_percent = float(sys.argv[3])
    print("Resizing {} by {}% in h axis and by {}% in v axis".format(imagepath, h_percent, v_percent))

    customImage.reduceByPercent(h_percent/100, v_percent/100)

if __name__ == "__main__":
    main()
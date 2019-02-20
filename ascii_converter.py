import os
from ImageMatrix import ImageMatrix

def main():

    src_dir = "source_images"
    target_dir = "converted_images"
    target_extra = "_ascii"
    scale_factor = 1
    font = "Fonts/arial.ttf"
    fontSize = 8
    letter = "@"
    threshold = 100
    for file in os.listdir(src_dir):
        if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
            print(file)
            img = ImageMatrix(src_dir + "/" + file)
            img.setDefaultFont(font)
            img.setDefaultFontSize(fontSize)
            img.setDefaultLetter(letter)
            img.monochrome(threshold)
            img.resize(img.getWidth()//scale_factor, img.getHeight()//scale_factor)
            img.initializeMatrix("random")
            img.saveMatrix(target_dir + "/" + file.replace(".png","").replace(".jpg","").replace(".jpeg","") + target_extra + ".png", format="img")

main()

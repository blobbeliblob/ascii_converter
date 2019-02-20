from os import listdir
from PIL import Image, ImageDraw, ImageFont
import random

class ImageMatrix():

    def __init__(self, src):
        self.img = None
        self.width, self.height = None, None
        self.matrix = None
        self.defaultLetter = "@"
        self.defaultFontPath = "Fonts/arial.ttf"    #must be truetype font
        self.defaultFontSize = 8
        self.characters = [chr(i) for i in range(ord('a'),ord('z')+1)]+[chr(i) for i in range(ord('A'),ord('Z')+1)]+["!","#","@","%","&","?"]
        try:
            self.img = Image.open(src)
            self.width, self.height = self.img.size
        except Exception as e:
            print("could not open image: "+src)
            print(e)

    def getDimensions(self):
        return (self.width, self.height)

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def setDefaultLetter(self, letter):
        try:
            self.defaultLetter = letter
        except Exception as e:
            print("could not set default letter")
            print(e)

    def setDefaultFont(self, font):
        try:
            self.defaultFontPath = font
        except Exception as e:
            print("could not set default font")
            print(e)

    def setDefaultFontSize(self, fontSize):
        try:
            self.defaultFontSize = fontSize
        except Exception as e:
            print("could not set default font size")
            print(e)

    #returns a cropped image
    def cropped(self, x, y, width, height):
        try:
            return self.img.crop((x, y, width, height))
        except Exception as e:
            print("could not crop image")
            print(e)
        return self.img

    #crops the image
    def crop(self, x, y, width, height):
        try:
            self.img = self.img.crop((x, y, width, height))
            self.width, self.height = self.img.size
        except Exception as e:
            print("could not crop image")
            print(e)

    #returns a resized image
    def resized(self, width, height):
        try:
            return self.img.resize((width, height))
        except Exception as e:
            print("could not resize image")
            print(e)
        return self.img

    #resizes the images
    def resize(self, width, height):
        try:
            self.img = self.img.resize((width, height))
            self.width, self.height = self.img.size
        except Exception as e:
            print("could not resize image")
            print(e)

    #returns a rotated image
    def rotated(self, angle):
        try:
            return self.img.rotate(angle)
        except Exception as e:
            print("could not rotate image")
            print(e)
        return self.img

    #rotates the image counter clockwise
    def rotate(self, angle):
        try:
            self.img = self.img.rotate(angle)
            self.width, self.height = self.img.size
        except Exception as e:
            print("could not rotate image")
            print(e)

    #returns a mirrored image
    def mirrored(self, direction):
        try:
            if direction == "horizontal":
                return self.img.transpose(Image.FLIP_LEFT_RIGHT)
            elif direction == "vertical":
                return self.img.transpose(Image.FLIP_TOP_BOTTOM)
            else:
                print("direction must be 'horizontal' or 'vertical'")
        except Exception as e:
            print("could not mirror image")
            print(e)
        return self.img

    #mirrors the image
    def mirror(self, direction):
        try:
            if direction == "horizontal":
                self.img = self.img.transpose(Image.FLIP_LEFT_RIGHT)
                self.width, self.height = self.img.size
            elif direction == "vertical":
                self.img = self.img.transpose(Image.FLIP_TOP_BOTTOM)
                self.width, self.height = self.img.size
            else:
                print("direction must be 'horizontal' or 'vertical'")
        except Exception as e:
            print("could not mirror image")
            print(e)

    #splits the image into different bands (red, green, blue), if specific is None -> returns all three in a tuple
    def splitRGB(self, specific=None):
        try:
            split_img = self.img.split()
            if not specific:
                return split_img
            else:
                if any(i in specific for i in ["RED","red","R","r"]):
                    return split_img[0]
                elif any(i in specific for i in ["GREEN","green","G","g"]):
                    return split_img[1]
                elif any(i in specific for i in ["BLUE","blue","B","b"]):
                    return split_img[2]
                else:
                    print("specific must be 'RED','GREEN' OR 'BLUE'")
        except Exception as e:
            print("could not split image")
            print(e)
        return None

    #turns image black and white, threshold if defined must be between 0 and 255
    def monochrome(self, threshold=None):
        try:
            if not threshold:
                self.img = self.img.convert("1")
            else:
                func = lambda x : 255 if x > threshold else 0
                self.img = self.img.convert("L").point(func, mode="1")
        except Exception as e:
            print("could not turn image black-and-white")
            print(e)

    #turns image into greyscale
    def greyscale(self):
        try:
            self.img = self.img.convert("L")
        except Exception as e:
            print("could not turn image into greyscale")
            print(e)

    #initialize the matrix, replace pixels (0,0,0) with defaultLetter and other pixels with blank space
    #remember to monochromise image before
    def initializeMatrix(self, letter=None):
        if not letter:
            letter = lambda: self.defaultLetter
        elif letter == "random":
            letter = lambda: self.characters[random.randint(0, len(self.characters)-1)]
        else:
            temp_str = letter
            letter = lambda: temp_str
        try:
            pixels = list(self.img.getdata())
            self.matrix = []
            for i in range(self.height):
                self.matrix.append([])
            for i in range(self.height):
                for k in range(self.width):
                    currentPixel = pixels[i * self.width + k]
                    self.matrix[i].append(letter() if self.darkPixel(currentPixel) else " ")
        except Exception as e:
            print("could not initialize matrix")
            print(e)

    #return true if the given pixel should be dark, false if it should be light
    def darkPixel(self, pix, threshold=0):
        if type(pix) is tuple:
            r, g, b = pix[0], pix[1], pix[2]
            if r + g + b == 0:
                return True
            else:
                return False
        else:
            if pix <= threshold:
                return True
            else:
                return False

    #saves matrix
    def saveMatrix(self, path, format="txt"):
        if format == "txt":
            try:
                matrix_file = open(path, "w")
                temp_str = ""
                for row in self.matrix:
                    for column in row:
                        temp_str += column
                    temp_str += "\n"
                matrix_file.write(temp_str)
                matrix_file.close()
            except Exception as e:
                print("could not save matrix as text")
                print(e)
        elif format == "img":
            try:
                temp_str = ""
                for row in self.matrix:
                    for column in row:
                        temp_str += column
                    temp_str += "\n"
                temp_img = self.convertMatrix(temp_str)
                temp_img.save(path)
            except Exception as e:
                print("could not save matrix as image")
                print(e)
        else:
            print("format not recognised, make sure it is either 'txt' or 'img'")

    #saves image
    def saveImage(self, path):
        try:
            self.img.save(path)
        except Exception as e:
            print("could not save image")
            print(e)

    #converts the matrix to an Image object and returns it
    def convertMatrix(self, matrix_str, fontPath=None, fontSize=None):
        if not fontPath:
            fontPath = self.defaultFontPath
        if not fontSize:
            fontSize = self.defaultFontSize
        split_matrix_str = matrix_str.split("\n")
        font = ImageFont.truetype(fontPath, fontSize)
        textColor = (0,0,0)
        pWidth = font.getsize(split_matrix_str[0])[0]/self.width
        pHeight = font.getsize(split_matrix_str[0])[1]
        pSize = pWidth if pWidth > pHeight else pHeight
        temp_img = Image.new('RGB',(self.width*pSize,self.height*pSize), color='white')
        d = ImageDraw.Draw(temp_img)
        #d.text((0,0), matrix_str, fill=textColor)
        for i in range(len(split_matrix_str)):
            for k in range(len(split_matrix_str[i])):
                d.text((k*pSize,i*pSize), split_matrix_str[i][k], fill=textColor)
        return temp_img

#load image
#source_path = "Images/source_pic.png"
#save_path_image = "Images/output.png"
#save_path_text = "Images/output.txt"
#test_image = ImageMatrix(source_path)

'''
    AVAILABLE METHODS

    get:
        getDimensions()
        getWidth()
        getHeight()

    returns an image:
        cropped(x, y, width, height)
        resized(width, height)
        rotated(angle)
        mirrored(direction)

    modifies image:
        crop(x, y, width, height)
        resize(width, height)
        rotate(angle)
        mirror(direction)
        splitRGB(specific)
        monochrome(threshold)
        greyscale()

    matrix methods:
        initializeMatrix()

    save methods:
        saveImage(path)
        saveMatrix(path [, format])
'''

#mirror image
#mirrored_image = test_image.mirror("horizontal").save(save_path)

#monochrome
#test_image.monochrome(100)

#greyscale
#test_image.greyscale()

#split into RGB
#test_image.splitRGB("RED")

#matrix
#test_image.resize(test_image.getWidth()//16, test_image.getHeight()//16)
#test_image.initializeMatrix("random")

#save image matrix object as image
#test_image.saveImage(save_path_image)

#save image matrix object
#test_image.saveMatrix(save_path_text)
#test_image.saveMatrix(save_path_image, format="img")

# ascii_converter

This python script (ascii_converter.py) utilises the ImageMatrix class defined in ImageMatrix.py to convert an image file into ascii_art using the following process:
* Make the image monochromatic
* Create a matrix, where a black pixel is represented by a letter and a white pixel by whitespace

The script converts all image files located in its source directory ("/source_images" by default) and places the converted files in the target directory ("/converted_images" by default). The files can be saved in either .txt or .png format. The following settings can be changed easily in the script:
* src_dir = the source directory
* target_dir = the target directory
* target_extra = appended to the names of the converted files
* scale_factor = should the image be resized before converting, this can prevent large converted image files
* font = location of the font to be used, by default, Arial is included in the "/Fonts" directory
* fontSize = size of the font, larger sizes affect the size of the converted image files
* letter = letter to be used as default in the ascii art
* method = leave as "random" to use random letters, otherwise, replace with the letter variable
* threshold = the threshold when converting to monochromatic, an integer between 0 and 255

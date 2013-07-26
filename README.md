EncryptTextInImage
==================

Just to practice python I developed a program to encrypt text into an existing or new image, and to extract the text back from the image


I didn't look through any of the conventional encryption algorithms for this, I just made it up in my head. Although I do have a few ideas to make this more secure, I'll probably do so in a later version.

The encryption algorithm does the following:
  1. Randomly selects a few initial parameters. These parameters are "start" which determines the row number of the image from which the algorithm will start encrypting the text into pixels, "space" which specifies how many pixels are left blank between encrypted pixels - so for example if "space" is 4, then every fourth pixel will be encrypted. The dimensions for the image are calculated based on the length of the text to be encrypted and the above 2 initial parameters. An image of said dimensions is created with random pixel values. If the user chooses to encrypt an existing image, then the function checks if the image is large enough to fit the text, given "space" and "start." If the text is too small then the dimensions may be < 10 but the initial parameters are at least 9 pixels wide and since start is at least 2, at least 11 pixels tall so the minimum size for the image is 10x11
  2. The initial parameters are inserted into the image. The pattern "white-black-white-black-white" is inserted into the first 5 and last 5 pixels of the image. This pattern helps the program express and determine if a given image is encrypted by this program. The 6th pixel holds the value of "start". The 7th pixel holds the value of "space." The 8th pixel signifies the number of pixels needed to store the length of the text. If the text is < 255 characters, the 8th pixel holds the value "1" and the 9th pixel holds the length of the text. Else, the length is divided over the next few pixels such that the sum of them (255 + 255 + ...) gives the total length of the text and the number of pixels required is stored in the 8th pixel.
  3. The text is then encrypted into the image by storing the ascii value of each character as the value of each pixel, "space" pixels apart.
  4. The image is then saved and the user is notified.

  
The decryption algorithm does the following:
  1. Checks if the image is a valid image i.e. if it was encrypted by this program by checking if the width is minimum 10 pixels and height is minimum 11 (see why in the encryption algorithm), and if the pattern "white-black-white-black-white" on the top left and bottom right corner exists.
  2. If all is well so far, the algorithm extracts the initial parameters from the image (start, space, length)
  3. The function then extracts the values of pixels from the image depending on the values of the initial parameters and displays it to the user

""" Python program to encrypt and decrypt text in an image.


The top left 5 pixels and bottom right 5 pixels will be WHITE BLACK WHITE BLACK WHITE iff the image is encrypted.
The 6th top left pixel holds the row number from which the encryption starts
The 7th top left pixel holds the spacing value. So if the value is 9, then every 9th pixel holds data starting from row number mentioned in pixel 6
The 8th pixel holds the number of pixels required to hold the length of the text
The next few pixels hold the length of the text"""

import PIL
import random
import numpy, Image
import math

#print ord('a')

def encrypt(text):
  #Section 1 -- Initialize encryption parameters and calculate how big the image needs to be to fit the text
	l = len(text)
	#The row number of the image from which encryption starts
	start = random.randrange(2, 9)
	
	#Spacing between encrypted pixels
	space = random.randrange(2,9)
	
	#Min image dimension
	d = math.ceil(math.sqrt(l * space))
	if d < 10:
		d = 10
	#print start, space, len(text), d
	imarray = numpy.random.rand(d + start + 1,d,3) * 255
	im = Image.fromarray(imarray.astype('uint8')).convert('L')
	#im.save('result_image.png')
	
	#Insert encryption parameters into image
	pixels = im.load()
	pixels[0,0] = 255
	pixels[1,0] = 0
	pixels[2,0] = 255
	pixels[3,0] = 0
	pixels[4,0] = 255
	pixels[d -1, d + start] = 255
	pixels[d-2, d + start] = 0
	pixels[d -3, d + start] = 255
	pixels[d -4, d + start] = 0
	pixels[d -5, d + start] = 255
	
	pixels[5,0] = start
	pixels[6,0] = space
	
	if l <= 255:
		pixels[7,0] = 1
		pixels[8,0] = l
	else:
		total_pixels_required = int(math.ceil(l/255.0))
		pixels[7,0] = total_pixels_required
		i = 0
		for i in range(total_pixels_required-1):
			pixels[8 + i, 0] = 255
		if l%255 == 0: pixels[8 + i + 1, 0] = 255
		else: pixels[8 + i + 1, 0] = l%255
		
		
	#im.save('secret_message.png')
	#Section 2 --- Insert plaintext into image
	"""pix_flat = np.asarray(im).flatten()
	for i in range(d+1, d+d, 2):
		pix_flat[i] = 255
	im.save('secret_message.png')"""
	
	row = start
	column = 0
	for ch in range(l):
		pixels[column, row] = ord(text[ch])
		column +=space
		if column >= d:
			column %= d
			row += 1
			
	im.save('secret_message.png')
	im.show()
	print "Success! Your secret message has been encrypted into secret_message.png"
	
	
	
def encrypt_existing_image(text):
	#Section 1 -- Initialize encryption parameters and calculate how big the image needs to be to fit the text
	l = len(text)
	#The row number of the image from which encryption starts
	start = random.randrange(2, 9)
	
	#Spacing between encrypted pixels
	space = random.randrange(2,9)
	
	#Min image dimension
	d = math.ceil(math.sqrt(l * space))
	if d < 10:
		d = 10
	#print start, space, len(text), d
	
	print "Enter the location of the image you'd like to encrypt your text in."
	try:
		loc = raw_input()
		im = Image.open(loc).convert('L')
	except:
		print "Invalid image file"
		exit(1)
	if im.size[0] < d and im.size[1] < d + start:
		print "This image is too small to fit your message!"
		exit(1)
	
	#imarray = numpy.random.rand(d + start + 1,d,3) * 255
	#im = Image.fromarray(imarray.astype('uint8')).convert('L')
	#im.save('result_image.png')
	
	#Insert encryption parameters into image
	w, h = im.size
	pixels = im.load()
	pixels[0,0] = 255
	pixels[1,0] = 0
	pixels[2,0] = 255
	pixels[3,0] = 0
	pixels[4,0] = 255
	pixels[w -1, h-1] = 255
	pixels[w-2, h-1] = 0
	pixels[w -3, h-1] = 255
	pixels[w -4, h-1] = 0
	pixels[w -5, h-1] = 255
	
	pixels[5,0] = start
	pixels[6,0] = space
	
	if l <= 255:
		pixels[7,0] = 1
		pixels[8,0] = l
	else:
		total_pixels_required = int(math.ceil(l/255.0))
		pixels[7,0] = total_pixels_required
		i = 0
		for i in range(total_pixels_required-1):
			pixels[8 + i, 0] = 255
		if l%255 == 0: pixels[8 + i + 1, 0] = 255
		else: pixels[8 + i + 1, 0] = l%255
		
		
	#im.save('secret_message.png')
	#Section 2 --- Insert plaintext into image
	"""pix_flat = np.asarray(im).flatten()
	for i in range(d+1, d+d, 2):
		pix_flat[i] = 255
	im.save('secret_message.png')"""
	
	row = start
	column = 0
	for ch in range(l):
		pixels[column, row] = ord(text[ch])
		column +=space
		if column >= w:
			column %= w
			row += 1
			
	im.save('secret_message.png')
	#im.show()
	print "Success! Your secret message has been encrypted into secret_message.png"
	
	
	
	
	
def decrypt(im):
	#Section 1 -- Confirm initial encryption parameters'
	pixels = im.load()
	w = im.size[0]
	h = im.size[1] - 1
	if w >= 10 and h >=11 and pixels[0,0] == 255 and pixels[1,0] == 0 and pixels[2,0] == 255 and pixels[3,0] == 0 and pixels[4,0] == 255 and pixels[w -1,  h] == 255 and pixels[w-2, h] == 0 and pixels[w -3, h] == 255 and pixels[w -4, h] == 0 and pixels[w -5, h] == 255:
		start = pixels[5,0]
		space = pixels[6,0]
		total_pixels_required = pixels[7,0]
		l = 0
		if total_pixels_required == 1:
			l = pixels[8,0]
		else:
			for i in range(total_pixels_required):
				l += pixels[8 + i, 0]
			
		#Section 2 --- Extract plaintext from image	
		plainText = ''
		row = start
		column = 0
		for ch in range(l):
			plainText += chr(pixels[column, row])
			column +=space
			if column >= w:
				column %= w
				row += 1
				
		print "Success! Your secret message has been extracted! The message is: \n\n"
		print plainText
	else:
		print "Hmm this picture doesn't seem to be encrypted by this program!"
	
	
def getPlainText():
	print "Enter the text you'd like to encrypt."
	return raw_input()
	
def getCipherImage():
	print "Enter the location of the image you'd like to decrypt."
	try:
		loc = raw_input()
		img = Image.open(loc)
		return img
	except:
		print "Invalid image file"
		exit(1)
	
def main():
	print "Welcome to Meenakshi's simple encryption engine."
	print "The way this works is as follows. You enter the text you want to encrypt. The program gives back an image with the text encrypted within in. You can then pass the image over to your friend. Your friend can pass the image to the program on her machine. The program will then give back to her your original text."
	print "Enter E if you want to send a secret message."
	print "Enter D if you want to receive a secret message."
	ed = raw_input()
	if ed.lower() == 'e':
		pt = getPlainText()
		print "Would you like to encrypt your message in an existing image? (y/n)"
		yn = raw_input()
		if yn.lower() == 'n':
			encrypt(pt)
		elif yn.lower() == 'y':
			encrypt_existing_image(pt)
		#TODO
		#Save the image in /ciphers
		#Display the image
		#Let the user know
		#ADVANCED - Offer the user to directly mail/send the image
	elif ed.lower() == 'd':
		decrypt(getCipherImage())
		#TODO
		#Display the text
		#Offer to save the text
		
		

main()

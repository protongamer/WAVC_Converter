#by protongamer 2018

import binascii
import os

print("WAVC Converter - by protongamer")
print("Drag your .wav file(mono unsigned 8 bit or signed 16 bit supported) to the same folder of WAV2C")
print("Enter file name")


snd = raw_input()


p = 0 #counter to read snd buffer
w = 1 #counter to fill new var buffer
slash = 0 #slash character detection
name_array = "" #name of the final array
while(snd[p] != '.'):
    p = p + 1
    if(snd[p] == "\\"):
        slash = p
        #print p

new = snd[0]
while(w < p):
    new = new + snd[w]
    w = w + 1
    
new = new + ".c"

w = slash
while(w < p):
    name_array = name_array + snd[w] #fill the name array
    w = w + 1
#print(name_array)

#print(new)

file=open(new,"w+") #create fill with the same name of selected file
with open(snd, 'rb') as f:
    content = f.read() #read bytes of bmp file

#calculate bits per sample, number of bytes and channel number of channels
a = list(content)

channels = (ord(a[23]) << 8) | ord(a[22]) #Number of channels(mono stereo)
bps = (ord(a[35]) << 8) | ord(a[34])	#Bits per sample
sam_r = (ord(a[27]) << 8) | (ord(a[26]) << 8) | (ord(a[25]) << 8) | ord(a[24]) #sample rate

if(channels == 2):
	print("\n\nError, wav file is stereo and actually unsupported by software")
	print("Press Enter to close...")
	raw_input()
	exit()

print("\nThe wav file is mono")
print "Bits per sample:",bps
print "Sample rate:",sam_r,"Hz"
endian = ""
if(bps == 16):
	print("\n16 bit detected !")
	print("Put raw bytes data in Big Endian ? Or keep it in Little Endian ?")
	
	while(endian != 'B' and endian != 'b' and endian != 'L' and endian != 'l'):
		endian = raw_input("Choose Endianness(B/L)")
		if(endian != 'B' and endian != 'b' and endian != 'L' and endian != 'l'):
			print("Error 42, choose right value\n")

if(endian == 'B' or endian == 'b'):
	print("\nBig Endian")

if(endian == 'L' or endian == 'l'):
	print("\nLittle Endian")

byte_size = 0	

#calculate number of raw bytes


byte_size = (ord(a[43]) << 24) | (ord(a[42]) << 16) | (ord(a[41]) << 8) | (ord(a[40]))

	

#print("Image width :",wh[0])
#print("Image height :",wh[1])
#print(data)
i = 0
h = 0
c1 = 0


if(bps == 8):
	file.write("const uint8_t "+ name_array +"[] = { \n")
	while(i < byte_size-1):
		
		h = ord(a[i+44])
		file.write("%s"%hex(h))
		file.write(",")
		c1 = c1 + 1
		i = i + 1
		if(c1 > 200):
			file.write("\n")
			c1 = 0
	h = ord(a[i+44])
	file.write("%s"%hex(h))
	file.write("\n};")
	file.close()
	
if(bps == 16):
	if(endian == 'B' or endian == 'b'):
		file.write("const uint16_t "+ name_array +"[] = { \n")
		while(i < byte_size - 2):
			h = 0
			h = (ord(a[i+44+1]) << 8) | ord(a[i+44])
			file.write("%s"%hex(h))
			file.write(",")
			c1 = c1 + 1
			i = i + 2
			if(c1 > 200):
				file.write("\n")
				c1 = 0
		h = (ord(a[i+44+1]) << 8) | ord(a[i+44])
		file.write("%s"%hex(h))
		file.write("\n};")
		file.close()
			
		
		
	if(endian == 'L' or endian == 'l'):
		file.write("const int16_t "+ name_array +"[] = { \n")
		while(i < byte_size - 2):
			h = 0
			h = (ord(a[i+44]) << 8) | ord(a[i+44+1])
			file.write("%s"%hex(h))
			file.write(",")
			c1 = c1 + 1
			i = i + 2
			if(c1 > 200):
				file.write("\n")
				c1 = 0
		h = (ord(a[i+44]) << 8) | ord(a[i+44+1])
		file.write("%s"%hex(h))
		file.write("\n};")
		file.close()
print "\nDone"
raw_input("Press Enter to close...")
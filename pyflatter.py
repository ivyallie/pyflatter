#!/usr/bin/python
#PyFlatter by John W. Allie
#www.johnwallie.com

import Image, ImageDraw, ImageColor, random, sys, timeit, subprocess, os, argparse

starttime=timeit.default_timer()

######Functions

def validPercent(value):
    #Evaluate an integer to see if it's a valid percentage between 1 and 99
    intval = int(value)
    if not 0 < intval < 100:
        raise argparse.ArgumentTypeError("Scale factor must be a percentage between 1 and 99")
    return intval


def flood(posx,posy,color):
    #flood an area starting at the specified pixel with the specified color
    ImageDraw.floodfill(im, (posx,posy), color, border=None)
    
def RandomColor():
    #Generate a random color with HSV values. Brightness is locked between 23-75% to prevent very light and
    #very dark colors from being produced. The returned value is encoded as RGB, not HSV.
    hue=random.randint(0,360)
    sat=random.randint(0,100)
    bright=random.randint(25,75)
    return ImageColor.getrgb("hsl("+str(hue)+","+str(sat)+"%,"+str(bright)+"%)")

def getAllPixels():
    #Evaluate every pixel in the image one by one
    dimensions=im.size
    
    for posy in range(dimensions[1]):
        for posx in range(dimensions[0]):
            CheckPixel(posx,posy)
            
def CheckPixel(posx,posy):
    #Determine whether the pixels need to be flooded
    pixelColor=(im.load()[posx,posy])
    if pixelColor==(255,255,255,255):
        #If pixel is white, fill with a random color
        flood(posx,posy,RandomColor())
    elif pixelColor==(0,0,0,255):
        #If pixel is black, fill with transparency
        flood(posx,posy,(255,255,255,0))
    else:
        pass
    
def elapsed():
    #Return how much time has elapsed
    if timeit.default_timer()-starttime < 60:
        return str(int(timeit.default_timer()-starttime))+" seconds"
    else:
        minutes=int((timeit.default_timer()-starttime)/60)
        if minutes==0 or minutes==1:
            return "1 minute"
        else:
            return str(minutes)+" minutes"


def closeGaps():
    #Invoke ImageMagick to close the gaps in the image.
    if GetImage():
        print("Closing gaps...")
        subprocess.call(["convert "+args.infile+" -negate -morphology Close Square:3 magick_output.png"], shell=True)
        subprocess.call(["mogrify -negate magick_output.png"], shell=True)
    
def voronoi():
    #Create the file to be passed to the voronoi script
    if not args.novor:
        if not args.scaling:
            im.save("voronoi_input.png", "PNG")
            print("Doing voronoi fill...")
            subprocess.call(["./voronoi.sh"], shell=True)
        else:
            #If scaling option is in use, scale the file before passing it to voronoi script, then when the
            #script has completed, scale it back up.
            scaleFactor=float(args.scaling)/100
            rsz = im.resize((int(im.size[0]*scaleFactor),int(im.size[1]*scaleFactor)))
            rsz.save("voronoi_input.png", "PNG")
            print("Doing the voronoi thing, please wait")
            subprocess.call(["./voronoi.sh"], shell=True)
            FinalImage = Image.open("output.png")
            finalrsz = FinalImage.resize((im.size[0],im.size[1]))
            finalrsz.save("output.png", "PNG")            
    else:
        #If voronoi is disabled, just save the final image.
        im.save("output.png", "PNG")
        
    CleanUp()
    
def CleanUp():
    #Get rid of temporary files if they exist, but don't crash if they don't
    try:
        os.remove("magick_output.png")
    except OSError:
        pass
    
    try:
        os.remove("voronoi_input.png")
    except OSError:
        pass
        
    
def FillRoutine():
    #Look for white pixels, then look for black pixels
    print("Creating color islands...")
    getAllPixels()
    print("Color islands completed at "+elapsed())
    
def GetImage():
    #Check if an image exists, then open it
    if os.path.exists(args.infile):
        global im
        im = Image.open(args.infile).convert('RGBA')
        return True
    else:
        print("Uh-oh! "+args.infile+" does not exist!")
        quit()
        
########Argparse options
parser = argparse.ArgumentParser(prog='PyFlatter', description="Create color flats for a black-and-white bitmap.")
parser.add_argument('-g', '--no-gaps', help='Disable gap handling', action="store_true", dest="nogaps")
parser.add_argument('-v', '--no-voronoi', help='Disable voronoi fill', action="store_true", dest="novor")
parser.add_argument('-s', '--scale', help='Scale the image by a given percentage to speed up voronoi processing', type=validPercent, dest="scaling", metavar=('PERCENTAGE'))
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument('infile', help='Input file', type=str)

args = parser.parse_args()

######The actual script

if args.nogaps:
    #If we're not handling gaps
    GetImage()
    FillRoutine()
    voronoi()
    
else:
    #If we are handling gaps
    closeGaps()
    im = Image.open("magick_output.png").convert('RGBA')
    FillRoutine()
    voronoi()


print("Script completed at "+elapsed())

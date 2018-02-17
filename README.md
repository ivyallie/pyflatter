# pyflatter
Create color flats for line drawings

PyFlatter brings automatic color flatting to Linux! "Color flatting" is the process of adding color shapes to black-and-white linework. Traditionally this was done manually, but computers can handle the task pretty well, using random colors that can easily be replaced with the correct colors later. Plugins to do this in Photoshop have been around for a while, but us Linux fans have been out of luck--until now!

PyFlatter uses the Python Image Library and ImageMagick to automate color flatting right from the Linux user's favorite tool--the command line! Just give it your linework and out comes a lovely set of color flats, ready to be imported into the image editor of your choice.

Visit http://www.johnwallie.com/pyflatter to see image examples.

## Features
- **Gap handling** PyFlatter will attempt to overlook any gaps in your linework so that shapes don't need to be completely enclosed to be filled in.
- **Voronoi fill** To ensure complete coverage, the color islands expand to fill the black areas of your image.
- **Temporary scaling** To speed up the voronoi process, the script can operate on a smaller version of the image, then scale it up to the correct size when it's done.


## Usage
It's very easy: **pyflatter.py inputfile.png** and you're off! You can also use these nifty options:
- **-g** Disable gap handling
- **-v** Disable voronoi fill
- **-s 50** Voronoi scale factor. Change 50 to whatever percentage you desire.

## Limitations
- Your input image must have black and white pixels only--no gray pixels allowed! Use the Threshold tool in your favorite image editor to accomplish this, and save in a lossless format such as PNG.
- The higher the resolution, the slower the voronoi process will be. If you have a big image (say, more than 2000 pixels in either dimension), it may take a _very_ long time. To compensate, either turn voronoi off entirely or set a smaller scale factor, such as 50%.
- Right now the output file is always a PNG. Hopefully that's not too inconvenient for anyone.
- Images with cross-hatching are not handled well.

## Changelog
1.1 - Improved PEP 8 conformity.
      Eliminated need for ImageMagick to support pipes. 
      Made temp files get written to /tmp instead of working directory.
1.0 - Initial version

## But I want to run it on Windows!

Maybe in the future, young padawan. But the time is not yet ripe.

## Credit where credit is due

Thanks to fmw42 on the ImageMagick forums for helping me figure out how to get the voronoi working, and Snibgo for showing me the workaround for pipes.

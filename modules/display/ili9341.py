import time
import busio
import digitalio
import board

from PIL import Image
from adafruit_rgb_display import color565
import adafruit_rgb_display.ili9341 as ili9341


# Configuration for CS and DC pins:
cs = digitalio.DigitalInOut(board.CE0)
rs = digitalio.DigitalInOut(board.D25)
dc = digitalio.DigitalInOut(board.D24)
baudrate = 24000000



class ILI9341():
    
    config = None
    display = None
    
    def __init__(self, config):
        self.config = config
        # Setup SPI bus using hardware SPI:
        spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        # Create the ILI9341 display:
        self.display = ili9341.ILI9341(spi, cs=cs,dc=dc,rst=rs, width=320, height=240,baudrate=baudrate)
    
    def clear(self):
        self.display.fill(0)
  
    def update(self,im_array):
        if self.config.G_QUIT:
            return
        image = Image.frombytes("1", 
        (im_array.shape[1]*8, im_array.shape[0]),
        (~im_array).tobytes()
      )
        image_resized = image.resize((self.display.width, self.display.height))
        image = image_resized.convert("RGB")
        self.display.image(image)
      

      
        
    
    
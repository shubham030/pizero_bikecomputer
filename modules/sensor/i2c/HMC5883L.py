import time
import numpy as np

try:
  #run from top directory (pizero_bikecomputer)
  from . import i2c
except:
  #directly run this program
  import i2c

### HMC5883L Register definitions ###
Register_A     = 0              #Address of Configuration register A
Register_B     = 0x01           #Address of configuration register B
Register_mode  = 0x02           #Address of mode register

X_axis_H    = 0x03              #Address of X-axis MSB data register
Z_axis_H    = 0x05              #Address of Z-axis MSB data register
Y_axis_H    = 0x07              #Address of Y-axis MSB data register

class HMC5883L(i2c.i2c):
  #address
  SENSOR_ADDRESS = 0x1e # HMC5883L address

  #for reset
  RESET_ADDRESS = 0
  RESET_VALUE = 0

  #for test
  TEST_ADDRESS = None
  TEST_VALUE = (None)
  
  elements = ()
  elements_vec = ('mag_raw')

  def reset_value(self):
    for key in self.elements:
      self.values[key] = np.nan
    for key in self.elements_vec:
      self.values[key] = [0] * 3
  
  def init_sensor(self):
    #write to Configuration Register A
    self.bus.write_byte_data(self.SENSOR_ADDRESS, Register_A, 0x70)

    #Write to Configuration Register B for gain
    self.bus.write_byte_data(self.SENSOR_ADDRESS, Register_B, 0xa0)

    #Write to mode Register for selecting mode
    self.bus.write_byte_data(self.SENSOR_ADDRESS, Register_mode, 0)

  def read(self):
    self.read_mag()

  def read_mag(self):
    #Read raw data from X, Y and Z axis
    x = self.read_raw_data(X_axis_H)
    y = self.read_raw_data(Y_axis_H)
    z = self.read_raw_data(Z_axis_H)
    self.values['mag_raw'] = [x, y, z]
    
  def read_raw_data(self,addr):
    #Read raw 16-bit value
    high = self.bus.read_byte_data(self.SENSOR_ADDRESS, addr)
    low = self.bus.read_byte_data(self.SENSOR_ADDRESS, addr+1)
    
    #concatenate higher and lower value
    value = ((high << 8) | low)
        
    #to get signed value from mpu6050
    if(value > 32768):
        value = value - 65536
    return value


if __name__=="__main__":
  l = HMC5883L()
  while True:
    l.read()
    print("{:+.1f}, {:+.1f}, {:+.1f}".format(
      l.values['mag_raw'][0],
      l.values['mag_raw'][1],
      l.values['mag_raw'][2],
      ))
    time.sleep(0.1)



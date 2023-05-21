import time
import numpy as np

try:
  #run from top directory (pizero_bikecomputer)
  from . import i2c
except:
  #directly run this program
  import i2c

### MPU6050 Register definitions ###
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

class MPU6050(i2c.i2c):
  #address
  SENSOR_ADDRESS = 0x68

  #for test
  TEST_ADDRESS = None
  TEST_VALUE = (None)
  
  elements = ()
  elements_vec = ('acc', 'gyro')

  def reset_value(self):
    for key in self.elements:
      self.values[key] = np.nan
    for key in self.elements_vec:
      self.values[key] = [0] * 3
  
  def init_sensor(self):
    # write to sample rate register
    self.bus.write_byte_data(self.SENSOR_ADDRESS, SMPLRT_DIV, 7)
    # Write to power management register
    self.bus.write_byte_data(self.SENSOR_ADDRESS, PWR_MGMT_1, 1)
	  # Write to Configuration register
    self.bus.write_byte_data(self.SENSOR_ADDRESS, CONFIG, 0)
	  # Write to Gyro configuration register
    self.bus.write_byte_data(self.SENSOR_ADDRESS, GYRO_CONFIG, 24)
	  # Write to interrupt enable register
    self.bus.write_byte_data(self.SENSOR_ADDRESS, INT_ENABLE, 1)

  def read(self):
    self.read_acc()
    self.read_mag()

  def read_acc(self):
    #Read the accelerometer and return the x, y and z acceleration as a vector in Gs.
    x = self.read_raw_data(ACCEL_XOUT_H)
    y = self.read_raw_data(ACCEL_YOUT_H)
    z = self.read_raw_data(ACCEL_ZOUT_H)
    self.values['acc'] = [x, y, z]
    
  def read_gyro(self):
    #Read the gyro and return the raw x, y and z axis values.
    x = self.read_raw_data(GYRO_XOUT_H)
    y = self.read_raw_data(GYRO_YOUT_H)
    z = self.read_raw_data(GYRO_ZOUT_H)
    self.values['gyro'] = [x, y, z]

  def read_raw_data(self,addr):
	  #Accelerometer and Gyro value are 16-bit
    high = self.bus.read_byte_data(self.SENSOR_ADDRESS, addr)
    low = self.bus.read_byte_data(self.SENSOR_ADDRESS, addr+1)
    
    #concatenate higher and lower value
    value = ((high << 8) | low)
        
    #to get signed value from mpu6050
    if(value > 32768):
        value = value - 65536
    return value


if __name__=="__main__":
  l = MPU6050()
  while True:
    l.read()
    print("{:+.1f}, {:+.1f}, {:+.1f}, {:+.1f}, {:+.1f}, {:+.1f}".format(
      l.values['acc'][0],
      l.values['acc'][1],
      l.values['acc'][2],
      l.values['gyro'][0],
      l.values['gyro'][1],
      l.values['gyro'][2],
      ))
    time.sleep(0.1)



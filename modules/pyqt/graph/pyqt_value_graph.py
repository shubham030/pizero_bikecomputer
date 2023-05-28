import numpy as np
import pyqtgraph as pg

from modules.pyqt.pyqt_screen_widget import ScreenWidget

pg.setConfigOptions(antialias=True)
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


class PerformanceGraphWidget(ScreenWidget):

  def init_extra(self):
    self.display_item = self.config.G_GUI_PERFORMANCE_GRAPH_DISPLAY_ITEM
    self.item = {
      'POWER': {
        'name':'POWER',
        'graph_key': 'power_graph',
        'yrange':[self.config.G_GUI_MIN_POWER, self.config.G_GUI_MAX_POWER],
      },
      'HR': {
        'name':'HR',
        'graph_key': 'hr_graph',
        'yrange':[self.config.G_GUI_MIN_HR, self.config.G_GUI_MAX_HR],
      },
      'W_BAL': {
        'name':'W_BAL',
        'graph_key': 'w_bal_graph',
        'yrange':[self.config.G_GUI_MIN_W_BAL, self.config.G_GUI_MAX_W_BAL],
      },

    }
    self.plot_data_x1 = []
    for i in range(self.config.G_GUI_PERFORMANCE_GRAPH_DISPLAY_RANGE):
      self.plot_data_x1.append(i)

  def setup_ui_extra(self): 
    #1st graph: POWER
    self.plot = pg.PlotWidget()
    self.plot.setBackground(None)
    self.p1 = self.plot.plotItem

    #2nd graph: HR or W_BAL
    self.p2 = pg.ViewBox()
    self.p1.showAxis('right')
    self.p1.scene().addItem(self.p2)
    self.p1.getAxis('right').linkToView(self.p2)
    self.p2.setXLink(self.p1)

    self.plot.setXRange(0, self.config.G_GUI_PERFORMANCE_GRAPH_DISPLAY_RANGE)
    self.p1.setYRange(*self.item[self.display_item[0]]['yrange'])
    self.p2.setYRange(*self.item[self.display_item[1]]['yrange'])
    self.plot.setMouseEnabled(x=False, y=False)
    
    #self.p1.setLabels(left=self.item[self.display_item[0]]['name'])
    #self.p1.getAxis('right').setLabel(self.display_item[self.item[1]]['name'])

    #p2 on p1
    self.p1.setZValue(-100)
  
    #for Power
    #self.brush = pg.mkBrush(color=(0,160,255,64))
    self.brush = pg.mkBrush(color=(0,255,255))
    #self.pen2 = pg.mkPen(color=(255,255,255,0), width=0.01) #transparent and thin line
    self.pen1 = pg.mkPen(color=(255,255,255), width=0.01) #transparent and thin line
    #for HR, wbal
    self.pen2 = pg.mkPen(color=(255,0,0), width=2)

  def make_item_layout(self):
    #self.item_layout = {"Power":(0, 0), "HR":(0, 1), "Lap PWR":(0, 2), "LapTime":(0, 3)}
    self.item_layout = {"Power":(0, 0), "HR":(0, 1), "W'bal(Norm)":(0, 2), "LapTime":(0, 3)}

  def add_extra(self):
    self.layout.addWidget(self.plot, 1, 0, 2, 4)

  def set_border(self):
    self.max_height = 1
    self.max_width = 3

  def set_font_size(self, length):
    self.font_size = int(length / 7)
    self.set_minimum_size()

  async def update_extra(self):
    #all_nan = {'hr_graph': True, 'power_graph': True}
    all_nan = {self.item[self.display_item[0]]['graph_key']: True, self.item[self.display_item[1]]['graph_key']: True}
    for key in all_nan.keys():
      chk = np.isnan(self.config.logger.sensor.values['integrated'][key])
      if False in chk:
        all_nan[key] = False
   
    if not all_nan[self.item[self.display_item[0]]['graph_key']]:
      self.p1.clear()

      #change max for power
      if self.display_item[0] == 'POWER':
        power_max = 100 * (int(np.nanmax(self.config.logger.sensor.values['integrated'][self.item[self.display_item[0]]['graph_key']])/100) + 1)
        if self.item[self.display_item[0]]['yrange'][1] != power_max:
          self.item[self.display_item[0]]['yrange'][1] = power_max
          self.p1.setYRange(*self.item[self.display_item[0]]['yrange'])

      self.p1.addItem(
        pg.BarGraphItem(
          x0 = self.plot_data_x1[:-1],
          x1 = self.plot_data_x1[1:],
          height = self.config.logger.sensor.values['integrated'][self.item[self.display_item[0]]['graph_key']],
          brush = self.brush,
          pen = self.pen1
        )
      )

    #if not all_nan['hr_graph']:
    if not all_nan[self.item[self.display_item[1]]['graph_key']]:
      self.p2.clear()
      self.p2.setGeometry(self.p1.vb.sceneBoundingRect())
      self.p2.linkedViewChanged(self.p1.vb, self.p2.XAxis)
      #for HR
      self.p2.addItem(
        pg.PlotCurveItem(
          #self.config.logger.sensor.values['integrated']['hr_graph'], 
          self.config.logger.sensor.values['integrated'][self.item[self.display_item[1]]['graph_key']], 
          pen=self.pen2
        )
      )


class AccelerationGraphWidget(ScreenWidget):

  def init_extra(self):
    pass

  def setup_ui_extra(self): 
    self.plot = pg.PlotWidget()
    self.plot.setBackground(None)
    self.p1 = self.plot.plotItem
    self.p1.showGrid(y=True)
    #self.p1.setLabels(left='HR')
    
    self.p2 = pg.ViewBox()
    self.p1.scene().addItem(self.p2)
    self.p2.setXLink(self.p1)
    self.p3 = pg.ViewBox()
    self.p1.scene().addItem(self.p3)
    self.p3.setXLink(self.p1)

    self.plot.setXRange(0, self.config.G_GUI_ACC_TIME_RANGE)
    self.plot.setMouseEnabled(x=False, y=False)
    #pg.setConfigOptions(antialias=True)
  
    #for acc
    self.pen1 = pg.mkPen(color=(0,0,255), width=3)
    self.pen2 = pg.mkPen(color=(255,0,0), width=3)
    self.pen3 = pg.mkPen(color=(0,0,0), width=2)
    
    self.g_range = 0.5
  
  def start(self):
    self.timer.start(self.config.G_REALTIME_GRAPH_INTERVAL)

  def make_item_layout(self):
    self.item_layout = {"ACC_X":(0, 0), "ACC_Y":(0, 1), "ACC_Z":(0, 2), "M_Stat":(0, 3)}

  def add_extra(self):
    self.layout.addWidget(self.plot, 1, 0, 2, 4)

  def set_border(self):
    self.max_height = 1
    self.max_width = 3

  def set_font_size(self, length):
    self.font_size = int(length / 15)
    self.set_minimum_size()

  async def update_extra(self):

    X = 0
    Y = 1
    Z = 2
    
    v = self.config.logger.sensor.sensor_i2c.graph_values['g_acc']
    all_nan = {X: True, Y: True, Z: True}
    for key in all_nan.keys():
      chk = np.isnan(v[key])
      if False in chk:
        all_nan[key] = False
    m = [x for x in v[0] if not np.isnan(x)]
    median = None
    if len(m) > 0:
      median = m[-1]
   
    if not all_nan[X]:
      self.p1.clear()
      if median != None:
        self.p1.setYRange(-self.g_range, self.g_range)

      self.p1.addItem(
        pg.PlotCurveItem(
          v[X], 
          pen=self.pen1,
          connect="finite"
        )
      )

    if not all_nan[Y]:
      self.p2.clear()
      
      if median != None:
        self.p2.setYRange(-self.g_range, self.g_range)
      
      self.p2.setGeometry(self.p1.vb.sceneBoundingRect())
      self.p2.linkedViewChanged(self.p1.vb, self.p2.XAxis)
      p = pg.PlotCurveItem(
        v[Y], 
        pen=self.pen2,
        connect="finite"
        )
      self.p2.addItem(p)

    if not all_nan[Z]:
      self.p3.clear()
      
      if median != None:
        self.p3.setYRange(-self.g_range, self.g_range)
      
      self.p3.setGeometry(self.p1.vb.sceneBoundingRect())
      self.p3.linkedViewChanged(self.p1.vb, self.p3.XAxis)
      p = pg.PlotCurveItem(
        v[Z], 
        pen=self.pen3,
        connect="finite"
        )
      self.p3.addItem(p)


class AltitudeGraphWidget(ScreenWidget):

  def init_extra(self):
    pass
    #self.plot_data_x1 = []
    #for i in range(self.config.G_GUI_PERFORMANCE_GRAPH_DISPLAY_RANGE):
    #  self.plot_data_x1.append(i)

  def setup_ui_extra(self): 
    self.plot = pg.PlotWidget()
    self.plot.setBackground(None)
    self.p1 = self.plot.plotItem
    self.p1.showGrid(y=True)
    
    self.p2 = pg.ViewBox()
    self.p1.scene().addItem(self.p2)
    self.p2.setXLink(self.p1)

    self.plot.setXRange(0, self.config.G_GUI_PERFORMANCE_GRAPH_DISPLAY_RANGE)
    self.plot.setMouseEnabled(x=False, y=False)
    #pg.setConfigOptions(antialias=True)
  
    #for altitude_raw
    self.pen1 = pg.mkPen(color=(0,0,0), width=2)
    self.pen2 = pg.mkPen(color=(255,0,0), width=3)

    self.y_range = 15
    self.y_shift = 0 #self.y_ra  nge * 0.25

  def make_item_layout(self):
    self.item_layout = {"Grade":(0, 0), "Grade(spd)":(0, 1), "Altitude":(0, 2), "Alt.(GPS)":(0, 3)}

  def add_extra(self):
    self.layout.addWidget(self.plot, 1, 0, 2, 4)

  def set_border(self):
    self.max_height = 1
    self.max_width = 3

  def set_font_size(self, length):
    self.font_size = int(length / 15)
    self.set_minimum_size()

  async def update_extra(self):
   
    v = self.config.logger.sensor.values['integrated']
    all_nan = {'altitude_graph': True, 'altitude_gps_graph': True}
    for key in all_nan.keys():
      chk = np.isnan(v[key])
      if False in chk:
        all_nan[key] = False
    m = [x for x in v['altitude_graph'] if not np.isnan(x)]
    median = None
    if len(m) > 0:
      median = m[-1]
   
    if not all_nan['altitude_graph']:
      self.y_range = max(abs(min(v['altitude_graph'])-median),abs(max(v['altitude_graph'])-median))

      if np.isnan(self.y_range) or self.y_range < 15:
        self.y_range = 15
      else:
        self.y_range = 10*(int(self.y_range/10)+1)

      self.p1.clear()
      if median != None:
        self.p1.setYRange(median-self.y_range, median+self.y_range)

      self.p1.addItem(
        pg.PlotCurveItem(
          v['altitude_graph'], 
          pen=self.pen1,
          connect="finite"
        )
      )

    if not all_nan['altitude_gps_graph']:
      self.p2.clear()
      
      if median != None:
        self.p2.setYRange(median-self.y_range+self.y_shift, median+self.y_range+self.y_shift)
      
      self.p2.setGeometry(self.p1.vb.sceneBoundingRect())
      self.p2.linkedViewChanged(self.p1.vb, self.p2.XAxis)
      p = pg.PlotCurveItem(
        v['altitude_gps_graph'], 
        pen=self.pen2,
        connect="finite"
        )
      self.p2.addItem(p)


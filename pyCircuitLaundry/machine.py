from .timestamp import *

class Machine:
    def __init__(self, app_data, pos_data=None, rot=None, top=False):
        self._app_type = app_data["t"]
        self._state = app_data["st"]
        self._number = app_data["ch"]
        self._model = app_data["md"] if "md" in app_data else None
        self._label = app_data["lbl"]
        
        self._dimensions = (
            app_data["dim"]["x"], 
            app_data["dim"]["z"], 
            app_data["dim"]["y"])
        
        self._position = (
            app_data["pos"]["x"], 
            app_data["pos"]["z"], 
            app_data["pos"]["y"] + top * self._dimensions[2])
        
        self._rotation = rot if rot else app_data["rot"]
        
        
        self._xon = to_datetime(app_data["xon"]) if "xon" in app_data else None
        self._xoff = to_datetime(app_data["xoff"]) if "xoff" in app_data else None
        self._cycle_count = app_data["cycles"] if "cycles" in app_data else None
    
    @property
    def app_type(self): return self._app_type
    
    @property
    def state(self): return self._state
    
    @property
    def number(self): return self._number
    
    @property
    def model(self): return self._model
    
    @property
    def label(self): return self._label
    
    @property
    def dimensions(self): return self._dimensions
    
    @property
    def position(self): return self._position
    
    @property
    def rotation(self): return self._rotation
    
    @property
    def xon(self): return self._xon
    
    @property
    def xoff(self): return self._xoff
    
    @property
    def cycle_count(self): return self._cycle_count
    
    @property
    def average_cycle(self): return self._average_cycle

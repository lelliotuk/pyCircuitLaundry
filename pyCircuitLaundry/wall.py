class Wall:
    def __init__(self, wall_data):
        self._dimensions = (
            (wall_data["x1"], wall_data["z1"]), 
            (wall_data["x2"], wall_data["z2"]))
                            
        self._visible = wall_data["show"]
        self._label = wall_data["label"]

    @property
    def dimensions(self): return self._dimensions
    
    @property
    def visible(self): return self._visible
    
    @property
    def label(self): return self._label

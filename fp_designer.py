#/usr/bin/env python3

class Initialisable:
    """Initialise an object with a list of args, store them as private"""
    def __init__(self, **kwargs):
        for arg, value in kwargs.items():
            setattr(self, arg, value)

    def __setattr__(self, name, value):
        super().__setattr__('_'+name, value)
        
    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError
        return getattr(self, '_'+name)

class Pad(Initialisable):
    PAD_CALCS = {
        "width": ["self._right-self._left", 
                  "2*(self._hcenter-self._left)", 
                  "2*(self._right-self._hcenter)"],
        "left": ["self._right-self._width",
                 "self._hcenter-self._width/2",
                 "self._right - (self._right-self._hcenter)*2"],
        "right": ["self._left + self._width",
                  "self._left + (self._hcenter-self._left)*2",
                  "self._hcenter + self._width/2"],
        "hcenter": ["(self._right - self._left)/2",
                    "self._right - self._width/2",   
                    "self._left + self_width/2"],
        "height": ["self._bottom-self._top", 
                  "2*(self._vcenter-self._top)", 
                  "2*(self._bottom-self._vcenter)"],
        "top": ["self._bottom-self._height",
                 "self._vcenter-self._height/2",
                 "self._bottom - (self._bottom-self._vcenter)*2"],
        "bottom": ["self._top + self._height",
                  "self._top + (self._vcenter-self._top)*2",
                  "self._vcenter + self._height/2"],
        "vcenter": ["(self._bottom - self._top)/2",
                    "self._bottom - self._height/2",   
                    "self._top + self_height/2"]                    
        }

    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError
        if '_'+name in self.__dict__:
            return getattr(self, '_'+name)
        if hasattr(self.parent,name):
            return getattr(self.parent, name)
        if name in self.PAD_CALCS:
            for code in self.PAD_CALCS[name]:
                try:
                    return eval(code)
                except AttributeError:
                    pass    
        raise AttributeError
                   
    def __init__(self, parent, **kwargs):
        self.parent = parent
        super().__init__(**kwargs)
        
    def get_pad(self):
        dct = {}
        if self.width > self.height:
            dct["y1"] = self.vcenter
            dct["y2"] = self.vcenter
            dct["thickness"] = self.height
            dct["x1"] = self.left + self.height/2
            dct["x2"] = self.right - self.height/2
        else:
            dct["x1"] = self.hcenter
            dct["x2"] = self.hcenter
            dct["thickness"] = self.width
            dct["y1"] = self.top + self.width/2
            dct["y2"] = self.bottom - self.width/2
        return "Pad [{x1} {y1} {x2} {y2} {thickness} 1 1 \"1\" \"1\"]".format(**dct)


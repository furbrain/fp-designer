#/usr/bin/env python3

def sine(x):
    return math.sin(math.pi*x/180.0)
    
def cosine(x):
    return math.cos(math.pi*x/180.0)

class Initialisable:
    """Initialise an object with a list of args, store them as private"""
    def __init__(self, **kwargs):
        for arg, value in kwargs.items():
            setattr(self, arg, value)


class CalculateVars:
    def __setattr__(self, name, value):
        super().__setattr__('_'+name, value)
        
    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError
        if '_'+name in self.__dict__:
            return getattr(self, '_'+name)
        if hasattr(self.parent,name):
            if self.parent:
                return getattr(self.parent, name)
        if name in self.CALCS:
            for code in self.CALCS[name]:
                try:
                    return eval(code)
                except AttributeError:
                    pass
        raise AttributeError


class Pad(Initialisable, CalculateVars):
    CALCS = {
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
                    "self._left + self._width/2"],
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
                    "self._top + self._height/2"],
        "name": ["str(self.number)"],
        "name": ["1"],
        "number": ["1"],
        "round": ['False'],
        "units": ['"mm"']             
        }

                   
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.parent.add(self)
        super().__init__(**kwargs)
        
    def get_text(self):
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
        dct["x1"] -= self.offsetx
        dct["x2"] -= self.offsetx
        dct["y1"] -= self.offsety
        dct["y2"] -= self.offsety
        dct["name"] = self.name
        dct["number"] = self.number
        dct["clearance"] = self.clearance
        dct["mask"] = self.mask*2+dct["thickness"]
        dct["units"] = self.units
        if self.round:
            dct["flags"] = ""
        else:
            dct["flags"] = "square"
        return 'Pad [{x1}{units} {y1}{units} {x2}{units} {y2}{units} {thickness}{units} {clearance}{units} {mask}{units} "{name}" "{number}" "{flags}"]\n'.format(**dct)
        
class HLine(Initialisable, CalculateVars):
    CALCS = {
        "width": ["self.length"],
        "length": ["self._right-self._left", 
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
                    "self._left + self._width/2"],
        "height": ["self.thickness"],
        "thickness": ["self._bottom-self._top", 
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
                    "self._top + self._height/2"],
    }
    
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.parent.add(self)
        super().__init__(**kwargs)

    def get_text(self):
        dct = {}
        dct["y1"] = self.vcenter
        dct["y2"] = self.vcenter
        dct["thickness"] = self.height
        dct["x1"] = self.left
        dct["x2"] = self.right
        dct["x1"] -= self.offsetx
        dct["x2"] -= self.offsetx
        dct["y1"] -= self.offsety
        dct["y2"] -= self.offsety
        dct["units"] = self.units
        return 'ElementLine [{x1}{units} {y1}{units} {x2}{units} {y2}{units} {thickness}{units}]\n'.format(**dct)


class VLine(Initialisable, CalculateVars):
    CALCS = {
        "height": ["self.length"],
        "width": ["self.thickness"],
        "thickness": ["self._right-self._left", 
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
                    "self._left + self._width/2"],
        "length": ["self._bottom-self._top", 
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
                    "self._top + self._height/2"],
        "round": ['False'],
        "units": ['"mm"']
    }

    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.parent.add(self)
        super().__init__(**kwargs)

    def get_text(self):
        dct = {}
        dct["x1"] = self.hcenter
        dct["x2"] = self.hcenter
        dct["thickness"] = self.width
        dct["y1"] = self.top
        dct["y2"] = self.bottom
        dct["x1"] -= self.offsetx
        dct["x2"] -= self.offsetx
        dct["y1"] -= self.offsety
        dct["y2"] -= self.offsety
        dct["units"] = self.units
        return 'ElementLine [{x1}{units} {y1}{units} {x2}{units} {y2}{units} {thickness}{units}]\n'.format(**dct)

class Line(Initialisable, CalculateVars):
    CALCS = {
        "x2": ["x1 + cosine(self.angle) * self.length"],
        "y2": ["y1 + sine(self.angle) * self.length"]
    }

    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.parent.add(self)
        super().__init__(**kwargs)

    def get_text(self):
        dct = {}
        dct["x1"] = self.x1
        dct["x2"] = self.x2
        dct["thickness"] = self.thickness
        dct["y1"] = self.y1
        dct["y2"] = self.y2
        dct["x1"] -= self.offsetx
        dct["x2"] -= self.offsetx
        dct["y1"] -= self.offsety
        dct["y2"] -= self.offsety
        dct["units"] = self.units
        return 'ElementLine [{x1}{units} {y1}{units} {x2}{units} {y2}{units} {thickness}{units}]\n'.format(**dct)

class PCB(Initialisable, CalculateVars):
    CALCS = {
        "clearance": ["0.25"],
        "mask": ["0.20"],
        "round": ['False'],
        "units": ['"mm"']        
    }

    def __init__(self, **kwargs):
        self.parent = None
        self.children = []
        super().__init__(**kwargs)
        
    def add(self, *items):
        self.children.extend(items)

    def get_text(self, center=True, outline=None, outline_thickness=0.5):
        minx = min(x.left for x in self.children)
        maxx = max(x.right for x in self.children)
        miny = min(x.top for x in self.children)
        maxy = max(x.bottom for x in self.children)
        if center:
            self.offsetx = (minx + maxx)/2
            self.offsety = (miny + maxy)/2
        else:
            self.offsetx = 0
            self.offsety = 0
        if outline:
            HLine(self, left=minx-outline, right=maxx+outline, vcenter=maxy+outline, thickness=outline_thickness)
            HLine(self, left=minx-outline, right=maxx+outline, vcenter=miny-outline, thickness=outline_thickness)
            VLine(self, top=maxy+outline, bottom=miny-outline, hcenter=minx-outline, thickness=outline_thickness)
            VLine(self, top=maxy+outline, bottom=miny-outline, hcenter=maxx+outline, thickness=outline_thickness)
            
        
        text = ''
        start = 'Element ["" "{name}" "" "" 0 0 0 0 0 100 ""] (\n'
        end = ')\n'
        text += start.format(name=self.name)
        for child in self.children:
            text += child.get_text()
        text += end
        return text

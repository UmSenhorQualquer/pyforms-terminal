
from pyforms_terminal.controls.control_base import ControlBase

class ControlCheckBox(ControlBase):

    def __init__(self, *args, **kwargs):
        if 'default' not in kwargs:
            kwargs['default'] = False
        super().__init__(*args, **kwargs)

    @property
    def value(self): return self._value

    @value.setter
    def value(self, value): ControlBase.value.fset(self, (value=='True' or value==True) )
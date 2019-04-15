#!/usr/bin/python
# -*- coding: utf-8 -*-

""" pyforms.gui.Controls.ControlList

"""
import logging
from pyforms_terminal.controls.control_base import ControlBase


logger = logging.getLogger(__name__)


class ControlList(ControlBase):
    """ This class represents a wrapper to the table widget
        It allows to implement a list view
    """
    def __init__(self, *args, **kwargs):
        if 'default' not in kwargs: kwargs['default'] = None
        super(ControlList, self).__init__(*args, **kwargs)

    def clear(self, headers=False):
        pass

    def save_form(self, data, path=None):
        data['value'] = self.value
        return data

    def load_form(self, data, path=None):
        self.value = data.get('value', [])

    def __add__(self, other):
        self.value.append(other)
        return self


    def __sub__(self, other):
        self.value.remove(other)
        return self

    def set_value(self, column, row, value):
        self.value[row][column] = value

    def get_value(self, column, row):
        return self.value[row][column]

    def resize_rows_contents(self):
        pass

    def get_currentrow_value(self):
        return None

    def get_cell(self, column, row):
        return None

    def set_sorting_enabled(self, value):
        pass

    ##########################################################################
    ############ EVENTS ######################################################
    ##########################################################################

    def data_changed_event(self, row, col, item):
        pass

    def item_selection_changed_event(self):
        pass

    def current_cell_changed_event(self, next_row, next_col, previous_row, previous_col):
        pass

    def current_item_changed_event(self, current, previous):
        pass

    def cell_double_clicked_event(self, row, column):
        pass

    ##########################################################################
    ############ PROPERTIES ##################################################
    ##########################################################################


    @property
    def horizontal_headers(self):
        return self._horizontalHeaders

    @horizontal_headers.setter
    def horizontal_headers(self, horizontal_headers):
        """Set horizontal headers in the table list."""

        self._horizontalHeaders = horizontal_headers

        
    @property
    def word_wrap(self):
        return True

    @word_wrap.setter
    def word_wrap(self, value):
        pass

    @property
    def readonly(self):
        return False

    @readonly.setter
    def readonly(self, value):
        pass

    @property
    def select_entire_row(self):
        pass

    @select_entire_row.setter
    def select_entire_row(self, value):
        pass

    @property
    def rows_count(self):
        return len(self.value) if self.value else 0

    @property
    def columns_count(self):
        return len(self.value[0]) if self.rows_count>0 else 0

    def __len__(self):
        return len(self.value) if self.value is not None else 0

   
    # TODO: implement += on self.value? I want to add a list of tuples to
    # self.value

    @property
    def selected_rows_indexes(self):
        return None

    @property
    def selected_row_index(self):
        pass

    @property
    def icon_size(self):
        return 0

    @icon_size.setter
    def icon_size(self, value):
        pass

    @property
    def autoscroll(self): return False
    @autoscroll.setter
    def autoscroll(self, value): pass


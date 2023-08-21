from __future__ import absolute_import, division, print_function

import os

from qtpy import QtWidgets
from glue_qt.utils import load_ui
from echo.qt import autoconnect_callbacks_to_qt

__all__ = ['AladinLiteOptionsPanel']


class AladinLiteOptionsPanel(QtWidgets.QWidget):

    def __init__(self, parent=None, viewer_state=None):

        super(AladinLiteOptionsPanel, self).__init__(parent=parent)

        self._data_collection = self.parent()._data

        self.viewer_state = viewer_state

        self.ui = load_ui('options_widget.ui', self,
                          directory=os.path.dirname(__file__))

        autoconnect_callbacks_to_qt(self.viewer_state, self.ui)

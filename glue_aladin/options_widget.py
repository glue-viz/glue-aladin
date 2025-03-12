from __future__ import absolute_import, division, print_function

import os

from qtpy import QtWidgets
from glue_qt.utils import load_ui
from echo.qt import autoconnect_callbacks_to_qt

__all__ = ['AladinLiteOptionsPanel']


class AladinLiteOptionsPanel(QtWidgets.QWidget):

    def __init__(self, parent=None, viewer_state=None, session=None):

        super(AladinLiteOptionsPanel, self).__init__(parent=parent)

        self.viewer_state = viewer_state

        self.ui = load_ui('options_widget.ui', self,
                          directory=os.path.dirname(__file__))

        self._connections = autoconnect_callbacks_to_qt(self.viewer_state, self.ui)

        self.viewer_state.add_callback('coordinate_grid', self._enable_grid_color)
        self.viewer_state.add_callback('reticle', self._enable_reticle_color)

        self._enable_grid_color(self.viewer_state.coordinate_grid)
        self._enable_reticle_color(self.viewer_state.reticle)

    def _enable_grid_color(self, grid):
        self.ui.color_coordinate_grid_color.setEnabled(grid)

    def _enable_reticle_color(self, reticle):
        self.ui.color_reticle_color.setEnabled(reticle)

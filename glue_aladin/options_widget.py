from __future__ import absolute_import, division, print_function

import os

from qtpy import QtWidgets
from glue.utils.qt import load_ui
from glue.core.qt.data_combo_helper import ComponentIDComboHelper
from glue.external.echo.qt import autoconnect_callbacks_to_qt
from glue.utils import nonpartial

__all__ = ['AladinLiteOptionsPanel']


class AladinLiteOptionsPanel(QtWidgets.QWidget):

    def __init__(self, parent=None, viewer_state=None):

        super(AladinLiteOptionsPanel, self).__init__(parent=parent)

        self._data_collection = self.parent()._data

        self.viewer_state = viewer_state

        self.ui = load_ui('options_widget.ui', self,
                          directory=os.path.dirname(__file__))

        autoconnect_callbacks_to_qt(self.viewer_state, self.ui)

        self._ra_att_helpers = ComponentIDComboHelper(self.ui.combodata_ra_att,
                                                      self._data_collection,
                                                      categorical=False,
                                                      default_index=0)

        self._dec_att_helpers = ComponentIDComboHelper(self.ui.combodata_dec_att,
                                                       self._data_collection,
                                                       categorical=False,
                                                       default_index=1)

        self.viewer_state.add_callback('layers', nonpartial(self._update_data))

    def _update_data(self):
        datasets = [layer.layer for layer in self.viewer_state.layers]
        self._ra_att_helpers.set_multiple_data(datasets)
        self._dec_att_helpers.set_multiple_data(datasets)

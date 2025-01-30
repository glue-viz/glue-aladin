import os
from echo.qt import autoconnect_callbacks_to_qt

from qtpy.QtWidgets import QWidget
from glue_qt.utils import load_ui


class AladinLiteCatalogOptionsPanel(QWidget):

    def __init__(self, layer_artist=None):

        super(AladinLiteCatalogOptionsPanel, self).__init__()

        self.layer_state = layer_artist.state

        self.ui = load_ui('catalog_layer_widget.ui', self,
                          directory=os.path.dirname(__file__))

        self._connections = autoconnect_callbacks_to_qt(self.layer_state, self.ui)

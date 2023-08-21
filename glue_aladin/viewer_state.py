from glue.viewers.common.state import ViewerState
from glue.core.data_combo_helper import ComponentIDComboHelper

from echo import SelectionCallbackProperty, ListCallbackProperty


class AladinLiteState(ViewerState):

    ra_att = SelectionCallbackProperty(default_index=0)
    dec_att = SelectionCallbackProperty(default_index=1)

    def __init__(self, **kwargs):

        super(AladinLiteState, self).__init__()

        self.add_callback('layers', self._layers_changed)

        self._ra_att_helpers = ComponentIDComboHelper(self, 'ra_att',
                                                      categorical=False)

        self._dec_att_helpers = ComponentIDComboHelper(self, 'dec_att',
                                                       categorical=False)

        self.add_callback('layers', self._layers_changed)

    def _layers_changed(self, *args):

        layers_data = self.layers_data
        layers_data_cache = getattr(self, '_layers_data_cache', [])

        if layers_data == layers_data_cache:
            return

        self._ra_att_helpers.set_multiple_data(self.layers_data)
        self._dec_att_helpers.set_multiple_data(self.layers_data)

        self._layers_data_cache = layers_data

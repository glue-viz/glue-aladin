from glue.viewers.common.state import ViewerState
from glue.core.data_combo_helper import ComponentIDComboHelper

from echo import CallbackProperty, SelectionCallbackProperty


class AladinLiteState(ViewerState):

    ra_att = SelectionCallbackProperty(default_index=0)
    dec_att = SelectionCallbackProperty(default_index=1)
    projection = SelectionCallbackProperty(default_index=2)
    reticle = CallbackProperty(False)
    reticle_color = CallbackProperty("#b2329e")
    coordinate_grid = CallbackProperty(False)
    coordinate_frame = SelectionCallbackProperty(default_index=0)
    coordinate_grid_color = CallbackProperty("#b2329e")

    _PROJECTIONS = {
        "AIT": "Hammer-Aïtoff",
        "SIN": "Spheric",
        "TAN": "Tangential",
        "MOL": "Mollweide",
        "MER": "Mercator",
        "ZEA": "Zenital equal-area",
        "STG": "Stereographic",
    }

    def __init__(self, **kwargs):

        super(AladinLiteState, self).__init__()

        self.add_callback('layers', self._layers_changed)

        self._ra_att_helpers = ComponentIDComboHelper(self, 'ra_att',
                                                      categorical=False)

        self._dec_att_helpers = ComponentIDComboHelper(self, 'dec_att',
                                                       categorical=False)
        AladinLiteState.projection.set_choices(self, list(AladinLiteState._PROJECTIONS.keys()))
        AladinLiteState.projection.set_display_func(self, AladinLiteState._PROJECTIONS.__getitem__)
        AladinLiteState.coordinate_frame.set_choices(self, ["ICRS", "ICRSd", "Galactic"])

        self._layers_changed()

    def _layers_changed(self, *args):

        layers_data = self.layers_data
        layers_data_cache = getattr(self, '_layers_data_cache', [])

        if layers_data == layers_data_cache:
            return

        self._ra_att_helpers.set_multiple_data(self.layers_data)
        self._dec_att_helpers.set_multiple_data(self.layers_data)

        self._layers_data_cache = layers_data

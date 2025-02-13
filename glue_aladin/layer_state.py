from __future__ import absolute_import, division, print_function

from glue.viewers.common.state import LayerState
from echo import CallbackProperty, SelectionCallbackProperty, keep_in_sync


class AladinLiteLayerState(LayerState):

    color = CallbackProperty()
    alpha = CallbackProperty()
    size = CallbackProperty(8)
    shape = SelectionCallbackProperty(
            default_index=0,
            choices=["square", "circle", "plus", "rhomb", "cross", "triangle"])

    def __init__(self, **kwargs):

        super(AladinLiteLayerState, self).__init__(**kwargs)

        self._sync_color = None
        self._sync_alpha = None

        self.add_callback('layer', self._layer_changed)
        self._layer_changed()

    def _layer_changed(self):

        if self._sync_color is not None:
            self._sync_color.stop_syncing()

        if self._sync_alpha is not None:
            self._sync_alpha.stop_syncing()

        if self.layer is not None:

            self.color = self.layer.style.color
            self.alpha = self.layer.style.alpha

            self._sync_color = keep_in_sync(self, 'color', self.layer.style, 'color')
            self._sync_alpha = keep_in_sync(self, 'alpha', self.layer.style, 'alpha')

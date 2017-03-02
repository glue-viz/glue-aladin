from __future__ import absolute_import, division, print_function

from glue.core.state_objects import State
from glue.external.echo import CallbackProperty


class AladinLiteLayerState(State):

    layer = CallbackProperty()
    visible = CallbackProperty(True)
    zorder = CallbackProperty(0)
    color = CallbackProperty()
    alpha = CallbackProperty()

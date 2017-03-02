from __future__ import absolute_import, division, print_function

from glue.core.state_objects import State
from glue.external.echo import CallbackProperty, ListCallbackProperty


class AladinLiteState(State):

    ra_att = CallbackProperty()
    dec_att = CallbackProperty()

    layers = ListCallbackProperty()

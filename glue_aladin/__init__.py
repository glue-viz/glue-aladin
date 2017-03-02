def setup():
    from .data_viewer import MyViewer
    from glue.config import qt_client
    qt_client.add(MyViewer)
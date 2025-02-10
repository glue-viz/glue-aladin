from glue.config import viewer_tool
from glue.viewers.common.tool import Tool
from glue_qt.utils import get_qapp
from qtpy.QtWidgets import QSystemTrayIcon


@viewer_tool
class AladinShareTool(Tool):

    def activate(self):
        app = get_qapp()
        cb = app.clipboard()
        cb.clear(mode=cb.Clipboard)

        def callback(url):
            icon = QSystemTrayIcon()
            icon.show()

            cb.dataChanged.connect(lambda: icon.showMessage(message))
            if url:
                cb.setText(url, mode=cb.Clipboard)
                message = "Share URL copied to clipboard"
            else:
                message = "Issue getting share URL"

        self.viewer.aladin_widget.run_js("aladin.getShareUrl()", callback)

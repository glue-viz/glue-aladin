def assert_js_result_equals(aladin_widget, js, expected):
    aladin_widget.run_js(js)
    assert(aladin_widget.page._js_response == expected)

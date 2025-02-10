def assert_js_result_satisfies(aladin_widget, js, condition):
    aladin_widget.run_js(js)
    assert condition(aladin_widget.page._js_response)


def assert_js_result_equals(aladin_widget, js, expected):
    print(expected)
    assert_js_result_satisfies(aladin_widget, js, lambda result: result == expected)

from time import sleep


def assert_js_result_equals(aladin_widget, js, expected):
    result = None
    def retain_result(res):
        print("RETAIN RESULT")
        global result
        result = res 
    aladin_widget.run_js(js, callback=retain_result)
    sleep(3)
    print(result)
    assert(result == expected)

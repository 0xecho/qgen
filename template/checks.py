def ends_with(suffix):
    def check(text):
        return text.endswith(suffix)
    return check
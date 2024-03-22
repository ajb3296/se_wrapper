
class LoginError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class UploadError(Exception):
    def __init__(self, msg):
        super().__init__(msg)
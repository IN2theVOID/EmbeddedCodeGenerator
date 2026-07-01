
class NoRoleMappingToUser(BaseException):
    pass

class FailedAuth(BaseException):
    pass

class ModelError(BaseException):
    pass

class DeployError(BaseException):
    pass
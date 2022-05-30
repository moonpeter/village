from rest_framework import exceptions, status


class PreconditionFailed(exceptions.APIException):
    status_code = status.HTTP_412_PRECONDITION_FAILED


class BAD_REQUEST(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class INTERNAL_SERVER_ERROR(exceptions.APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

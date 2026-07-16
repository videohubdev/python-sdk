class VideoHubError(Exception):
    pass


class AuthenticationError(VideoHubError):
    pass


class APIRequestError(VideoHubError):
    pass


class ValidationError(VideoHubError):
    pass
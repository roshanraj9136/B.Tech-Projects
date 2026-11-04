from fastapi import HTTPException, status

class VideoNotFoundError(HTTPException):
    def __init__(self, video_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Video with ID '{video_id}' not found."
        )

class AnalysisNotFoundError(HTTPException):
    def __init__(self, analysis_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis with ID '{analysis_id}' not found."
        )

class InvalidVideoFormatError(HTTPException):
    def __init__(self, message: str = "Invalid or unsupported video file format."):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )

class FileTooLargeError(HTTPException):
    def __init__(self, max_size_mb: int = 200):
        super().__init__(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Uploaded file exceeds maximum permitted size of {max_size_mb} MB."
        )

class ModelInferenceError(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Machine learning inference error: {message}"
        )

from .printout import error as iuerror
import cv2

class CameraReadError(ValueError):
    """Exception raised when the CameraCapture device is unable to
    read the camera
    """
    pass

class InvalidInterpolationType(TypeError):
    """
    Exception for an invalid interpolation Type where it's applicable

    Args:
        interp (cv2.constant): interpolation type
    """
    def __init__(self,interp):
        interp_string = """cv2.INTER_NEAREST --> {}
                        cv2.INTER_LINEAR --> {}
                        cv2.INTER_AREA --> {}
                        cv2.INTER_CUBIC --> {}
                        cv2.INTER_LANCZOS4 --> {}""".format(cv2.INTER_NEAREST,
                                                            cv2.INTER_LINEAR,
                                                            cv2.INTER_AREA,
                                                            cv2.INTER_CUBIC,
                                                            cv2.INTER_LANCZOS4)
        error_string = "'interpolation' ({}) must be one of the following!"\
                                                            .format(interp)
        error_string = error_string + '\n' + interp_string
        iuerror(error_string)
        super(InvalidInterpolationType,self).__init__(error_string)


class InvalidNumpyType(TypeError):
    """
    Exception for an invalid interpolation Type where it's applicable

    Args:
        dtype (np.dtype): numpy datatype
    """
    def __init__(self,dtype):
        error_string = "'dtype' ({}) must be one of the following!"\
                                                            .format(dtype)
        error_string += "\n\t".join(iu.NUMPY_TYPES)
        iuerror(error_string)
        super(InvalidNumpyType,self).__init__(error_string)

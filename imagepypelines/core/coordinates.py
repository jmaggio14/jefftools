# @Email: jmaggio14@gmail.com
# @Website: https://www.imagepypelines.org/
# @License: https://github.com/jmaggio14/imagepypelines/blob/master/LICENSE
# @github: https://github.com/jmaggio14/imagepypelines
#
# Copyright (c) 2018 Jeff Maggio, Nathan Dileas, Ryan Hartzell
def centroid(img):
    """finds the centroid of the given image img

    Args:
        img (np.ndarray):
            input img to find the centroid of
    Returns:
        tuple: centroid of the input image (height,width)

    Example:
        >>> import imagepypelines as ip
        >>> lenna_centroid = centroid( ip.lenna() )
    """
    centroid = img.shape[0]//2, img.shape[1]//2
    return centroid


def frame_size(img):
    """return the height and width of a given img

    Args:
        img (np.ndarray): input img to find frame_size of

    Returns:
        tuple: frame_size, height and width of the input img

    Example:
        >>> import imagepypelines as ip
        >>> lenna_framesize = frame_size( ip.lenna() )
    """
    frame_size = img.shape[0], img.shape[1]
    return frame_size


def dimensions(img, return_as_dict=False):
    """
    function which returns the dimensions and data_type of a given image

    Args:
        img (np.ndarray): input image
        return_as_dict (bool): whether or not to return a dictionary.
            Default is False

    Returns:
        tuple: dimensions of the form (rows, cols, bands, dtype)

    Example:
        >>> import imagepypelines as ip
        >>> dims = dimensions( ip.lenna() )
    """
    rows = img.shape[0]
    cols = img.shape[1]
    if img.ndim == 3:
        bands = img.shape[2]
    else:
        bands = 1
    dims = (rows, cols, bands, img.dtype)

    if return_as_dict:
        dims = dict(zip(('rows','cols','bands','dtype'), dims))

    return dims


# END
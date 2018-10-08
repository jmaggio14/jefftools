#
# @Email:  jmaggio14@gmail.com
#
# MIT License: https://github.com/jmaggio14/imsciutils/blob/master/LICENSE
#
# Copyright (c) 2018 Jeff Maggio, Nathan Dileas, Ryan Hartzell
#
from .. import SimpleBlock
import cv2
import numpy as np

class Orb(SimpleBlock):
    """Block to calculate ORB features upon input grayscale imagery

    Args:
        n_keypoints(int): maximum number of keypoints to detect

    Example:
        >>> import imsciutils as iu
        >>> orb = iu.ORB(n_keypoints=120)
        >>>
        >>> pipeline = iu.Pipeline()
        >>> pipeline.add( orb )
        >>>
        >>> lenna_gray = iu.lenna_gray()
        >>> lenna_gray_descriptors = pipeline.process( [lenna_gray] )[0]
    """
    def __init__(self,n_keypoints=100):
        if not isinstance(n_keypoints,(int,float)):
            error_msg = "'n_keypoints' must be int"
            self.printer.error(error_msg)
            raise TypeError(error_msg)

        self.n_keypoints = int(n_keypoints)
        self.orb = cv2.ORB_create(self.n_keypoints)

        input_shape = [None,None] #[Width,Height]
        output_shape = [None,32] #[n_keypoints_detected,32]
        super(Orb,self).__init__(input_shape=input_shape,
                                            output_shape=output_shape,
                                            requires_training=False)

    def process(self,datum):
        """calculates descriptors on a 4D img_stack (n_img,height,width,bands)

        If there are not enough keypoints calculated to populate the output
        array, the descriptor vectors will be replaced with zeros

        Args:
            datum (np.ndarray): image numpy array to process
                shape = (width,bands)

        Returns:
            descriptors(np.ndarray): 2D array of ORB descriptors
                shape = (n_keypoints,32)

        """
        _,des = self.orb.detectAndCompute(datum,None)
        return des
# @Email: jmaggio14@gmail.com
# @Website: https://www.imagepypelines.org/
# @License: https://github.com/jmaggio14/imagepypelines/blob/master/LICENSE
# @github: https://github.com/jmaggio14/imagepypelines
#
# Copyright (c) 2018 - 2020 Jeff Maggio, Jai Mehra, Ryan Hartzell
#
from .arg_checking import HOMOGENUS_CONTAINERS

import numpy as np

CONTAINER_REQUIRES = ['__getitem__', '__iter__', '__len__']

def is_container(data):
    return all(hasattr(data, req) for req in CONTAINER_REQUIRES)


class Data(object):
    """Object to batch lists or arrays as block processable data

    Attributes:
        data (any type): the raw data
    """
    def __init__(self, data):
        """instantiates the Data object

        Args:
            data (any type): the raw data container. A container is any
                type that can
                1) getitems -- i.e. container[i],
                2) iterate -- for datum in container,
                3) fetch length -- len(container)
        """
        # check if the data is a valid container
        if not is_container(data):
            msg = "invalid container type '%s' passed in. must have functions %s" % (type(data), CONTAINER_REQUIRES)
            raise TypeError(msg)

        self.data = data

    ############################################################################
    def n_batches_with(self, batch_type):
        """calculates the number of batches generated with the given batch_type"""
        if batch_type == "each":
            return self.n_datums
        elif batch_type == "all":
            return 1

    ############################################################################
    def as_all(self):
        """returns all the data in it's raw form"""
        return self.data

    ############################################################################
    def as_each(self):
        """returns a generator the returns each datum individually"""
        for d in self.data:
            yield d

    ############################################################################
    def pop(self):
        """returns the data, and then removes it from this object"""
        data = self.data
        self.data = None
        return data

    ############################################################################
    def grab(self):
        """returns the data in it's raw form"""
        return self.data

    ############################################################################
    def is_homogenus_container(self):
        """returns whether or not this container is homogenus"""
        is_homogenus = (type(self.data) in HOMOGENUS_CONTAINERS)

    ############################################################################
    def __len__(self):
        return len(self.data)

    ############################################################################
    #                               properties
    ############################################################################
    @property
    def n_datums(self):
        """int: number of items loaded into the pipeline"""
        return len(self)

    ############################################################################
    @property
    def datum_type(self):
        return type(self.data[0])

    ############################################################################
    @property
    def container_type(self):
        return type(self.data)

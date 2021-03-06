# @Email: jmaggio14@gmail.com
# @Website: https://www.imagepypelines.org/
# @License: https://github.com/jmaggio14/imagepypelines/blob/master/LICENSE
# @github: https://github.com/jmaggio14/imagepypelines
#
# Copyright (c) 2018-2020 Jeff Maggio, Ryan Hartzell, and collaborators
#
import sys
import inspect
from abc import abstractmethod
import copy
from types import FunctionType

from .Block import Block

this_module = sys.modules[__name__]


################################################################################
class PipelineBlock(Block):
    """Block which runs a pipeline internally (used for nesting pipelines
    within pipelines)

    Attributes:
        pipeline(:obj:`Pipeline`): pipeline to process with
        fetch(:obj:`tuple` of :obj:`str`): variables to fetch from the pipeline
            in the order to retrieve them in

    Batch Size:
        "each"
    """
    def __init__(self, pipeline, fetch):
        """instantiates the PipelineBlock

        Args:
            pipeline(:obj:`Pipeline`): pipeline to process with
            fetch(:obj:`tuple` of :obj:`str`): variables to fetch from the
                pipeline in the order to retrieve them in
        """
        # check to make sure all the fetch vars are actually in the pipeline
        if not all((fet in pipeline.vars) for fet in fetch):
            msg = "Invalid Pipeline fetch, must be one of %s" % pipeline.vars.keys()
            raise BlockError(msg)

        # instantiate block args
        self.fetch = fetch
        self.pipeline = pipeline
        # NOTE: do something here to support arg checking for the pipeline!!!

        super().__init__(name=pipeline.name, batch_type="all")


    ############################################################################
    def process(self, *args):
        """Runs the pipeline and fetches the desired variables"""
        # NOTE: we might want to make the pipeline's logger a child of this
        # block's logger in here?
        processed = self.pipeline.process(*args, fetch=self.fetch)

        # turn processed dict into a tuple of fetches
        return tuple(processed[fet] for fet in self.fetch)

    ############################################################################
    @property
    def args(self):
        """:obj:`list` of :obj:`str`: arg names for the pipeline"""
        return self.pipeline.args

################################################################################
class FuncBlock(Block):
    """Block that will run anmy fucntion you give it, either unfettered through
    the __call__ function, or with optional hardcoded parameters for use in a
    pipeline. Typically the FuncBlock is only used in the `blockify` decorator
    method.

    Attributes:
        func(function): the function to call internally
        preset_kwargs(dict): preset keyword arguments, typically used for
            arguments that are not data to process
    """
    # def __new__(self, func, preset_kwargs):
    #     return type(func.__name__+"FuncBlock", (SimpleBlock,), {})

    def __init__(self, func, preset_kwargs, **block_kwargs):
        """instantiates the function block

        Args:
            func (function): the function you desire to turn into a block
            preset_kwargs (dict): preset keyword arguments, typically used for
                arguments that are not data to process
            **block_kwargs: keyword arguments for :obj:`Block` instantiation
        """

        # JM: this is an ugly hack to make FuncBlock's serializable - by
        # adding the user's functions to the current namespace (pickle demands
        # the source object be in top level of the module)
        if not hasattr(this_module, func.__name__):
            func_copy = FunctionType(func.__code__, globals(), func.__name__)
            setattr(this_module, func_copy.__name__, func_copy)
        else:
            raise ValueError("illegal blockified function name: {}".format(func.__name__))

        self.func = func_copy
        self.preset_kwargs = preset_kwargs

        # check if the function meets requirements
        spec = inspect.getfullargspec(func)

        # we can't allow varargs at all because a block must have a known
        # number of inputs
        if (spec.varargs or spec.varkw):
            raise TypeError("function cannot accept a variable number of args")

        self._arg_spec = spec
        super().__init__(self.func.__name__,**block_kwargs)

    def process(self, *args):
        return self.func(*args, **self.preset_kwargs)

    def __call__(self, *args, **kwargs):
        """returns the exact output of the user defined function without any
        interference or interaction with the class
        """
        return self.func(*args,**kwargs)

    @property
    def args(self):
        """:obj:`list` of :obj:`str`: arguments in the order they are expected"""
        # save the argspec in an instance variable if it hasn't been computed
        if not self._arg_spec:
            self._arg_spec = inspect.getfullargspec(self.func)

        pos_args = ([] if (self._arg_spec.args is None) else self._arg_spec.args).copy()

        for idx,preset in enumerate(self.preset_kwargs.keys()):
            pos_args.remove(preset)

        return pos_args

################################################################################
class Input(Block):
    """An object to inject data into the graph

    Attributes:
        data(any type):
        loaded(bool): where
    """
    def __init__(self, index=None):
        """instantiates the Input

        Args:
            index(int,None): index of the input into the Pipeline
        """
        self.set_index(index)
        self.data = None
        super().__init__(name=self.name, batch_type="all")

    ############################################################################
    def process(self):
        """returns the loaded data"""
        if self.data is None:
            msg = "data not loaded"
            self.logger.error(msg)
            raise RuntimeError(msg)
        return self.data

    ############################################################################
    def load(self, data):
        """loads the given data for distribution into the pipeline"""
        self.data = data

    ############################################################################
    def unload(self):
        """unloads the data"""
        self.data = None

    ############################################################################
    def get_default_node_attrs(self):
        """retrieves default node attributes for the Input"""
        attrs = super().get_default_node_attrs()
        attrs['color'] = 'blue'
        attrs['shape'] = 'pentagon'
        return attrs

    ############################################################################
    def set_index(self, index):
        """sets the input index"""
        self.index = index
        self.name = "Input" + str(self.index)


    ############################################################################
    #                               properties
    ############################################################################
    @property
    def loaded(self):
        """bool: whether or not data has been loaded"""
        return (self.data is not None)

################################################################################
class Leaf(Block):
    """a block to act as a leaf node in the Pipeline Graph. Used to complete
    final outgoing edges from processing blocks

    Attributes:
        var_name(str): the name of the variable this leaf represents
    """
    def __init__(self,var_name):
        """instantiates the leaf

        Args:
            var_name(str): the name of the variable this leaf represents
        """
        self.var_name = var_name
        super().__init__(self.var_name, batch_type="all")

    ############################################################################
    def process(self,*data):
        """does nothing in a leaf"""
        pass
        # return data

    ############################################################################
    def _pipeline_process(self,*data, **kwargs):
        return data[0]

    ############################################################################
    def get_default_node_attrs(self):
        """retrieves default node attributes for the Leaf"""
        attrs = super().get_default_node_attrs()
        attrs['color'] = 'green'
        attrs['shape'] = 'ellipsis'
        return attrs

    ############################################################################
    #                               properties
    ############################################################################
    @property
    def args(self):
        """:obj:`list` of :obj:`str`: returns a 1-element list for this leaf's input"""
        return [self.var_name]


# END

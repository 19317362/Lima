#=============================================================================
#
# file :        Pilatus.py
#
# description : Python source for the Pilatus and its commands. 
#                The class is derived from Device. It represents the
#                CORBA servant object which will be accessed from the
#                network. All commands which can be executed on the
#                Pilatus are implemented in this file.
#
# project :     TANGO Device Server
#
# copyleft :    European Synchrotron Radiation Facility
#               BP 220, Grenoble 38043
#               FRANCE
#
#=============================================================================
#          This file is generated by POGO
#    (Program Obviously used to Generate tango Object)
#
#         (c) - Software Engineering Group - ESRF
#=============================================================================
#


import PyTango
import sys


#==================================================================
#   Pilatus Class Description:
#
#
#==================================================================


class Pilatus(PyTango.Device_4Impl):

#--------- Add you global variables here --------------------------

#------------------------------------------------------------------
#    Device constructor
#------------------------------------------------------------------
    def __init__(self,cl, name):
        PyTango.Device_4Impl.__init__(self,cl,name)
        self.init_device()

#------------------------------------------------------------------
#    Device destructor
#------------------------------------------------------------------
    def delete_device(self):
        pass


#------------------------------------------------------------------
#    Device initialization
#------------------------------------------------------------------
    def init_device(self):
        self.set_state(PyTango.DevState.ON)
        self.get_device_properties(self.get_device_class())

#==================================================================
#
#    Pilatus read/write attribute methods
#
#==================================================================

#------------------------------------------------------------------
#    Read Threshold_gain attribute
#------------------------------------------------------------------
    def read_Threshold_gain(self, attr):
        communication = _PilatusIterface.communication()
        gain = communication.gain()
        if gain is None:
            gain = -1
        attr.set_value(gain)


#------------------------------------------------------------------
#    Write Threshold_gain attribute
#------------------------------------------------------------------
    def write_Threshold_gain(self, attr):
        data = []
        attr.get_write_value(data)
        communication = _PilatusIterface.communication()
        threshold = communication.threshold()
        communication.set_threshold_gain(threshold,data[0])

#------------------------------------------------------------------
#    Read Threshold_value attribute
#------------------------------------------------------------------
    def read_Threshold_value(self, attr):
        communication = _PilatusIterface.communication()
        threshold = communication.threshold()
        if threshold == None:           # Not set
            threshold = -1
        attr.set_value(threshold)

#------------------------------------------------------------------
#    Write Threshold_value attribute
#------------------------------------------------------------------
    def write_Threshold_value(self, attr):
        data = []
        attr.get_write_value(data)
        communication = _PilatusIterface.communication()
        communication.set_threshold_gain(data[0])



#==================================================================
#
#    Pilatus command methods
#
#==================================================================

#==================================================================
#
#    PilatusClass class definition
#
#==================================================================
class PilatusClass(PyTango.DeviceClass):

    #    Class Properties
    class_property_list = {
        }


    #    Device Properties
    device_property_list = {
        }


    #    Command definitions
    cmd_list = {
        }


    #    Attribute definitions
    attr_list = {
        'Threshold_gain':
            [[PyTango.DevLong,
            PyTango.SCALAR,
            PyTango.READ_WRITE]],
        'Threshold_value':
            [[PyTango.DevLong,
            PyTango.SCALAR,
            PyTango.READ_WRITE]],
        }


#------------------------------------------------------------------
#    PilatusClass Constructor
#------------------------------------------------------------------
    def __init__(self, name):
        PyTango.DeviceClass.__init__(self, name)
        self.set_type(name)


#----------------------------------------------------------------------------
# Plugins
#----------------------------------------------------------------------------
from Lima import Core
from Lima.Pilatus import Interface

_PilatusIterface = None

def get_control() :
    global _PilatusIterface
    if _PilatusIterface is None:
        _PilatusIterface = Interface.Interface()
    return Core.CtControl(_PilatusIterface)

def close_interface() :
    global _PilatusIterface
    if _PilatusIterface is not None:
        _PilatusIterface.quit()
        _PilatusIterface = None


def get_tango_specific_class_n_device() :
    return PilatusClass,Pilatus

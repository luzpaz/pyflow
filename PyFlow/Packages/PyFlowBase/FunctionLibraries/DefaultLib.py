import os
import platform
from copy import copy, deepcopy
from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow import getHashableDataTypes
from PyFlow.Core.Common import *
from nine import IS_PYTHON2

class DefaultLib(FunctionLibraryBase):
    '''
    Default library builting stuff, variable types and conversions
    '''
    def __init__(self, packageName):
        super(DefaultLib, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', None, {"enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny| PinOptions.DictElementSuported, "constraint": "1", "structConstraint": "1"}),
                    meta={'Category': 'GenericTypes', 'Keywords': ['id'], "CacheEnabled": False})
    def copyObject(obj=('AnyPin', None, {"enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny| PinOptions.DictElementSuported, "constraint": "1", "structConstraint": "1"}), deepCopy=("BoolPin", False)):
        '''Shallow or deep copy of an object.'''
        copyFunction = deepcopy if deepCopy else copy
        return copyFunction(obj)

    @staticmethod
    @IMPLEMENT_NODE(returns=None, nodeType=NodeTypes.Callable, meta={'Category': 'DefaultLib', 'Keywords': []})
    def clearConsole():
        '''Cross platform clears console.'''
        system = platform.system()
        if system != "":
            system = system.lower()
            if system in ("windows", "win32"):
                os.system('cls')
            if system in ("linux", "darwin", "linux2"):
                os.system('clear')

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={'Category': 'GenericTypes', 'Keywords': []})
    def makeInt(i=('IntPin', 0)):
        '''Make integer.'''
        return i

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'GenericTypes', 'Keywords': []})
    def makeFloat(f=('FloatPin', 0.0)):
        '''Make floating point number.'''
        return f

    @staticmethod
    @IMPLEMENT_NODE(returns=('StringPin', ''), meta={'Category': 'GenericTypes', 'Keywords': []})
    def makeString(s=('StringPin', '')):
        '''Make string.'''
        return s

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'Math|Bool', 'Keywords': []})
    def makeBool(b=('BoolPin', False)):
        '''Make boolean.'''
        return b

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0, {"enabledOptions": PinOptions.AlwaysPushDirty}), meta={'Category': 'Utils', 'Keywords': [], "CacheEnabled": False})
    def clock():
        '''Returns the CPU time or real time since the start of the process or since the first call of process_time().'''
        if IS_PYTHON2:
            return time.clock()
        else:
            return time.process_time()

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', None, {"constraint": "3"}), meta={'Category': 'DefaultLib', 'Keywords': []})
    def select(A=('AnyPin', None, {"enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny | PinOptions.DictElementSuported}),
               B=('AnyPin', None, {"enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny | PinOptions.DictElementSuported}),
               PickA=('BoolPin', False),
               aPicked=("Reference", ("BoolPin", False))):
        '''
        If bPickA is true, A is returned, otherwise B.
        '''
        aPicked(PickA)
        return A if PickA else B

    @staticmethod
    @IMPLEMENT_NODE(returns=('StringPin', ""), meta={'Category': 'Utils', 'Keywords': []})
    def objectType(obj=("AnyPin", None, {"enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny | PinOptions.DictElementSuported})):
        '''Returns <u>type(obj).__name__</u>'''
        t = type(obj).__name__
        if t == "dictElement":
            t += ",key:{0},value:{1}".format(type(obj[1]).__name__, type(obj[0]).__name__)
        return t

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'DefaultLib', 'Keywords': ['in'], "CacheEnabled": False})
    def contains(obj=('AnyPin', None, {"constraint": "1", "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny | PinOptions.DictElementSuported}), element=("AnyPin", None, {"constraint": "1"})):
        """Python's <u>in</u> keyword. <u>element in obj</u> will be executed"""
        try:
            return element in obj
        except:
            return False

    @staticmethod
    @IMPLEMENT_NODE(returns=("AnyPin", None, {"constraint": "1", "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}),
                    meta={'Category': 'DefaultLib', 'Keywords': ['get'], "CacheEnabled": False})
    def getItem(obj=('AnyPin', None, {"constraint": "1", "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}),
                element=("AnyPin", None, {"supportedDataTypes": getHashableDataTypes() }),
                result=("Reference", ("BoolPin", False))):
        """Python's <u>[]</u> operator. <u>obj[element]</u> will be executed."""
        try:
            result(True)
            return obj[element]
        except:
            result(False)
            return None

    @staticmethod
    @IMPLEMENT_NODE(returns=("AnyPin", None, {"constraint": "1", "structConstraint": "1", "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'DefaultLib', 'Keywords': ['get'], 'CacheEnabled': False})
    def appendTo(obj=('AnyPin', None, {"constraint": "1", "structConstraint": "1", "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}),
                 element=("AnyPin", None, {"constraint": "1"}),
                 result=("Reference", ('BoolPin', False))):
        """Calls <u>obj.append(element)</u>. And returns object. If failed - object is unchanged"""
        try:
            obj.append(element)
            result(True)
            return obj
        except:
            result(False)
            return obj

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'DefaultLib', 'Keywords': ['get']})
    def addTo(obj=('AnyPin', None, {"constraint": "1", "structConstraint": "1", "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}),
              element=("AnyPin", None, {"constraint": "1"}),
              result=("Reference", ("AnyPin", None, {"constraint": "1", "structConstraint": "1", "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}))):
        """Calls <u>obj.add(element)</u>. And returns object. If failed - object is unchanged"""
        try:
            obj.add(element)
            result(obj)
            return True
        except:
            result(obj)
            return False
import ctypes
import os

# Load the DLL
dll_path = os.path.abspath("ArducamEvkSDK.dll")
sdk = ctypes.CDLL(dll_path)

# Example: calling a function (replace with real function name and args)
# sdk.FunctionName.restype = ctypes.c_int
# sdk.FunctionName.argtypes = [ctypes.c_int]
# result = sdk.FunctionName(123)

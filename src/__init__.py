import sys         #if sys is not there, put it in requirements.txt for installation, should be there by default tho
from src.logger import logging

def error_message_detail(error,error_detail:sys): #to push our own custom error message whenever error gets detected of type sys
    _,_,exc_tb=error_detail.exc_info() #Call error_detail.exc_info(), ignore the first two items (exception type and value), and store the traceback object in exc_tb for later use (like debugging or logging).
    file_name=exc_tb.tb_frame.f_code.co_filename #The file name of the source code where the exception occurred. tb_frame-frame object, frame.f_code - code object, code.co_filename- filename
    error_message="Error occured in python script name [{0}] line number [{1}] error message[{2}]".format(
     file_name,exc_tb.tb_lineno,str(error))#tb_lineno is an attribute of traceback object which gives the line no. where the error has occured

    return error_message

    

class CustomException(Exception): #inherits from base class Exception
    def __init__(self,error_message,error_detail:sys):  #constructor
        super().__init__(error_message)
        self.error_message=error_message_detail(error_message,error_detail=error_detail)
    
    def __str__(self):
        return self.error_message
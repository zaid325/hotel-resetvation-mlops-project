from src.logger import get_logger
from src.custom_exceptions import CustomException
import sys

logger=get_logger(__name__)

def test_custom_exception(a, b):
    try:
        result=a/b
        logger.info("dividing two numvers")
        return result

    except Exception as e:
        logger.error("an error occured") 
        raise CustomException("cant didvide by zero" , sys)
    
if __name__=="__main__":
    try:
        logger.info("starting the testing of custom exception")
        test_custom_exception(5, 0)

    except CustomException as ce:
        logger.error(str(ce))
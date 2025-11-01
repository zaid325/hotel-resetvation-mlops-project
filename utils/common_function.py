import os
import pandas as pd
from src.logger import get_logger
from src.custom_exceptions import CustomException
import yaml

logger=get_logger(__name__)

def read_yaml(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError("givn path is not valid")
        
        with open(file_path , "r") as yaml_file:
            config=yaml.safe_load(yaml_file)
            return config
            logger.info("sucessfully reading the yml file")

    except Exception as e:
        logger.error("failed to read the yaml file")
        raise CustomException("failed to read yaml file " , e)


def load_data(path):
    try:
        logger.info("loading data")
        return pd.read_csv(path)
    except Exception as e:
        logger.error("error" , e)
        raise CustomException("failed to load data" , e)
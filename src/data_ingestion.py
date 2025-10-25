import os
import pandas as pd 
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from config.paths_config import *
from src.custom_exceptions import CustomException
from utils.common_function import read_yaml

logger=get_logger(__name__)


class Data_ingestion:
    def __init__(self , config):
        sel.config=
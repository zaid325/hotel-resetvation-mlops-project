from src.custom_exceptions import CustomException
from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataProcessor
from src.model_traing import ModelTraining
from utils.common_function import read_yaml
from config.paths_config import *

if __name__=="__main__":

    ################################################################ DATA INGESTION ##########################################################################################################

    ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    ingestion.run()

####################################################################################### DATA PREPROCESSING #################################################################################################


    train_file_path=r"C:\Users\PC\mlops first project\artifact\raw\train.csv"
    test_file_path=r"C:\Users\PC\mlops first project\artifact\raw\test.csv"
    config_file_path=r'C:\Users\PC\mlops first project\config\config.yaml'
    processor=DataProcessor(train_file_path, test_file_path , PROCESSED_DIR , config_file_path)
    processor.process()


    ######################################################################## MODEL TRAINING #################################################################################################

    trainer=ModelTraining(PROCESSED_TRAINED_DATA_PATH , PROCESSED_TEST_DATA_PATH , MODEL_OUTPUT_PATH)
    trainer.run()



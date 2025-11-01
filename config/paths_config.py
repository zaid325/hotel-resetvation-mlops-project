import os


####################################################### DATA INGESTION ##############################################################
RAW_DIR="artifact/raw"
RAW_FILE_PATH=os.path.join(RAW_DIR , "raw.csv")
TRAIN_FILE_PATH=os.path.join(RAW_DIR , "train.csv")
TEST_FILE_PATH=os.path.join(RAW_DIR , "test.csv")

CONFIG_PATH="config/config.yaml"
gcp_credentials_path = r"C:\Users\PC\mlops first project\config\snappy-striker-475921-q4-a9df55b5c9c5.json"


############################# DATA PROCESSING############################################################################


PROCESSED_DIR= "artifact/processed"

PROCESSED_TRAINED_DATA_PATH=os.path.join(PROCESSED_DIR , "processed_train.csv")
PROCESSED_TEST_DATA_PATH=os.path.join(PROCESSED_DIR , "processed_test.csv")


###################################### MODEL TRAING##################################

MODEL_OUTPUT_PATH ="artifact/models/lgbm_model.pkl"


import os
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from config.paths_config import *
from src.custom_exceptions import CustomException
from utils.common_function import read_yaml
import sys
import os
from config.paths_config import gcp_credentials_path




logger = get_logger(__name__)

class DataIngestion:
    def __init__(self, config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.bucket_file_name = self.config["bucket_file_name"]
        self.train_test_ratio = self.config["train_ratio"]
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gcp_credentials_path
    
        os.makedirs(RAW_DIR, exist_ok=True)
        logger.info("Data ingestion initialized.")

    def download_csv_from_gcp(self):
        try:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\PC\mlops first project\config\snappy-striker-475921-q4-a9df55b5c9c5.json"

            print("🚀 Starting GCP download...")
            print(f"Bucket name: {self.bucket_name}")
            print(f"File name: {self.bucket_file_name}")

            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.bucket_file_name)

            blob.download_to_filename(RAW_FILE_PATH)
            logger.info("✅ CSV downloaded successfully from GCP bucket.")

        except Exception as e:
            logger.error(f"❌ Failed to download CSV from GCP: {e}")
            raise CustomException(e, sys)

    def split_data(self):
        try:
            data = pd.read_csv(RAW_FILE_PATH)
            train_data, test_data = train_test_split(
                data, train_size=self.train_test_ratio, random_state=42
            )

            train_data.to_csv(TRAIN_FILE_PATH, index=False)
            test_data.to_csv(TEST_FILE_PATH, index=False)

            logger.info("✅ Data successfully split into train and test sets.")
        except Exception as e:
            logger.error(f"❌ Error occurred while splitting data: {e}")
            raise CustomException(e, sys)

    def run(self):
        try:
            logger.info("🚀 Starting automated data ingestion pipeline...")
            self.download_csv_from_gcp()
            self.split_data()
            logger.info("✅ Data ingestion pipeline completed successfully.")
        except CustomException as ce:
            logger.error(str(ce))
            raise ce


if __name__ == "__main__":
    ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    ingestion.run()

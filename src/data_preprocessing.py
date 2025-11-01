import os
import pandas as pd
import numpy as np
from config.paths_config import*
from src.logger import get_logger
from src.custom_exceptions import CustomException
from utils.common_function import read_yaml,load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger=get_logger(__name__)


class DataProcessor:


    def __init__(self , train_path , test_path , processed_dir , config_path):
        self.train_path=train_path
        self.test_path=test_path
        self.processed_dir=processed_dir
        self.config=read_yaml(config_path)

        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)

    def preprocessed_data(self , df):
        try:
            logger.info("starting the data preprocessing")

            df.drop(columns=["Booking_ID"] , inplace=True)
            df.drop_duplicates(inplace=True)

            cat_cols=self.config["data_processing"]["categorical_columns"]
            num_cols=self.config["data_processing"]["numerical_columns"]

            label_encoder=LabelEncoder()

            mapping={}

            for col in cat_cols:
                df[col]=label_encoder.fit_transform(df[col])
                mapping[col]={label:code for label, code in zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_))}

            logger.info("label mappings are : ")
            for col,mapp in mapping.items():
                logger.info(f"{col} : {mapp}")

            logger.info("doing skewness handling")

            skewness_threshlold=self.config["data_processing"]["skewness_threshold"]
            skewness=df[num_cols].apply(lambda x : x.skew())

            for column in skewness[skewness>skewness_threshlold].index:
                df[column]=np.log1p(df[column])

            return df
        
        except Exception as e:
            logger.error(f"fail to pre-processed data {e}" )
            raise CustomException("pre processing of the data is unsucsessfull" , e)
        


    def balance_data(self , df):
        try:
            logger.info("handling missing data")
            x=df.drop(columns="booking_status")
            y=df["booking_status"]

            smote=SMOTE(random_state=42)
            x_resampled , y_resampled=smote.fit_resample(x , y)
            balanced_df=pd.DataFrame(x_resampled , columns=x.columns)
            balanced_df["booking_status"]=y_resampled

            logger.info("data balanced sucessfully")
            return balanced_df
        
        except Exception as e:
            logger.error(f"fail to balance the data {e}")
            raise CustomException("balanceing of the data is unsucsessfull" , e)
        


    def feature_selection(self , df):
        try:
            logger.info("doing the feature selection")
            x=df.drop(columns="booking_status")
            y=df["booking_status"]
            model=RandomForestClassifier()
            model.fit(x,y)
            important_features=model.feature_importances_
            important_feature_df=pd.DataFrame({
                                "features":x.columns,
                                "importance":important_features
                            })
            number_of_features=self.config["data_processing"]["top_features"]
            top_10_features=important_feature_df["features"].head(number_of_features).values
            top_10_df=df[top_10_features.tolist()+["booking_status"]]

            logger.info("the feature selection of the dataframe is sucessfull")
            return top_10_df
        
        except Exception as e:
            logger.error(f"fail to do the feature selection {e}" )
            raise CustomException("feature selection of the data is unsucsessfull" , e)
        

    def save_data(self , df , file_path):
        try:
            logger.info("save data in csv format in a processed folder")
            df.to_csv(file_path , index=False)

            logger.info(f"data saved succesfully to path{file_path}")
        except Exception as e:
            logger.error(f"failed to save the data {e}"  )
            raise CustomException(f"data saving was usecessufll ", e )
        
    def process(self):
        try:
            logger.info("loading data from raw dict")

            train_df=load_data(self.train_path)
            test_df=load_data(self.test_path)

            train_df=self.preprocessed_data(train_df)
            test_df=self.preprocessed_data(test_df)

            train_df=self.balance_data(train_df)
            test_df=self.balance_data(test_df)

            train_df=self.feature_selection(train_df)
            test_df=test_df[train_df.columns]

            self.save_data(train_df , PROCESSED_TRAINED_DATA_PATH)
            self.save_data(train_df , PROCESSED_TEST_DATA_PATH)

            logger.info("creating the dataframe and saving")

        except Exception as e:
            logger.error(f"error while pre processing pipeline {e}"  ,exc_info=True )
            raise CustomException("error while pre processing the pipeline" , e)
        

if __name__=="__main__":
    train_file_path=r"C:\Users\PC\mlops first project\artifact\raw\train.csv"
    test_file_path=r"C:\Users\PC\mlops first project\artifact\raw\test.csv"
    config_file_path=r'C:\Users\PC\mlops first project\config\config.yaml'
    processor=DataProcessor(train_file_path, test_file_path , PROCESSED_DIR , config_file_path)
    processor.process()





        


            

        


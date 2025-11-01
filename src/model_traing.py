import os 
import pandas as pd
import joblib
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb
from sklearn.metrics import accuracy_score , f1_score, recall_score , precision_score
from src.logger import get_logger
from src.custom_exceptions import CustomException
from config.paths_config import *
from config.model_params import *
from utils.common_function import read_yaml , load_data
from scipy.stats import randint
import mlflow
import mlflow.sklearn

logger=get_logger(__name__)

class ModelTraining:

    def __init__(self , train_path , test_path , model_output_path):
        logger.info("beggning of the model training")
        self.train_path=train_path
        self.test_path=test_path
        self.model_output_path=model_output_path

        self.params_dist=light_params
        self.random_search_parms=random_search_params

    def load_and_split_data(self):
        try:
            logger.info("loading the data for splitting") 
            train_df=load_data(self.train_path)

            logger.info("loading the data for splitting test") 
            test_df=load_data(self.test_path)

            x_train=train_df.drop(columns=["booking_status"])
            y_train=train_df["booking_status"]

            x_test=test_df.drop(columns=["booking_status"])
            y_test=test_df["booking_status"]

            logger.info("data splitted sucesfully")

            return x_train , y_train , x_test , y_test
    
        except Exception as e:
            logger.error(f"error while loading the data {e}")
            raise CustomException("failed to load data" ,e)
        
    def train_lgbm(self , x_train , y_train):
        try:
            logger.info("initializing out model training")

            lgbm_model=lgb.LGBMClassifier(random_state=self.random_search_parms["random_state"])

            logger.info("starting hyperparameter tuning")

            random_search=RandomizedSearchCV(
                estimator=lgbm_model,
                param_distributions=self.params_dist,
                n_iter=self.random_search_parms["n_iter"],
                cv=self.random_search_parms["cv"],
                n_jobs=self.random_search_parms["n_jobs"],
                verbose=self.random_search_parms["verbose"],
                random_state=self.random_search_parms["random_state"],
                scoring=self.random_search_parms["scoring"]
            )

            logger.info("starting model hyperparameter tuning")
            random_search.fit(x_train , y_train)

            best_params=random_search.best_params_
            best_lgbm_model=random_search.best_estimator_

            logger.info(f"best prams are {best_params}")
            return best_lgbm_model
        
        
        except Exception as e:
            logger.error(f"error while training and hypertuning the data {e}")
            raise CustomException("failed to train the model" ,e)
    
    def evaluate_model(self , model , x_test , y_test):
        try:
            logger.info("evaluating the model")

            y_pred=model.predict(x_test)
            accuracy=accuracy_score(y_test , y_pred)
            precesion=precision_score(y_test , y_pred)  
            recall=recall_score(y_test , y_pred)
            f1=f1_score(y_test , y_pred)

            logger.info(f"accuracy score: {accuracy}")
            logger.info(f"prescision score: {precesion}")
            logger.info(f"recall score: {recall}")
            logger.info(f"f1 score: {f1}")

            return{
                "accuracy":accuracy,
                "precesion":precesion,
                "recall":recall,
                "f1 score":f1

            }
        
        except Exception as e:
            logger.error(f"failed to evaluate the model {e}")
            raise CustomException("an error occured while evaluating the model" ,e)
        

    def saving_model(self , model):
        try:
            os.makedirs(os.path.dirname(self.model_output_path) , exist_ok=True)

            logger.info("saving the model")
            joblib.dump(model , self.model_output_path)
            logger.info("model sucesfully saved")

        except Exception as e:
            logger.error(f"failed to save model {e}")
            raise CustomException("an error occured while saving the model" ,e)
        

    def run(self):
        try:
            with mlflow.start_run():
                logger.info("starting our model training pipeline")
                logger.info("starting our experiment")
                logger.info("logging the train and testing dataset")
                mlflow.log_artifact(self.train_path , artifact_path="datasets")
                mlflow.log_artifact(self.test_path , artifact_path="datasets")
                x_train , y_train , x_test , y_test=self.load_and_split_data()
                best_lgbm_model=self.train_lgbm(x_train , y_train)
                metrics=self.evaluate_model(best_lgbm_model , x_test , y_test)
                self.saving_model(best_lgbm_model)
                logger.info("saving the model in to mlflow")
                mlflow.log_artifact(self.model_output_path)

                mlflow.log_params(best_lgbm_model.get_params())
                mlflow.log_metrics(metrics)

                logger.info("model traing is finally sucessfull")

        except Exception as e:
            logger.error(f"failed finalized and train the model {e}")
            raise CustomException("an error occured while finalizing and traing the model" ,e)
        
if __name__=="__main__":
    trainer=ModelTraining(PROCESSED_TRAINED_DATA_PATH , PROCESSED_TEST_DATA_PATH , MODEL_OUTPUT_PATH)
    trainer.run()

        

        




        


         
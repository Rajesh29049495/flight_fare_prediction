import pandas as pd
from ffp.exception import ffpException
from ffp.logger import logging
from ffp.config import mongo_client
import os, sys
import yaml

def get_collection_as_dataframe(database_name: str, collection_name: str)->pd.DataFrame():
    try:
        logging.info(f"Reading data from database: {database_name} and collection: {collection_name}")
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f"Found columns: {df.columns}")
        if "_id" in df.columns:
            logging.info(f"Dropping column: _id")
            df = df.drop("_id", axis= 1)
        logging.info(f"Row and columns in df: {df.shape}")
        return df
    except Exception as e:
        raise ffpException(e, sys)

##function to save data/report in '.yaml' file{the format}
def write_yaml_file(file_path, data:dict):
    try:
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir, exist_ok = True)
        with open(file_path, "w") as file_writer:
            yaml.dump(data, file_writer)
    except Exception as e:
        raise ffpException(e, sys)


def convert_columns_float(df:pd.DataFrame, exclude_columns:list)->pd.DataFrame:
    try:
        for column in df.columns:
            if column not in exclude_columns:
                df[column] = df[column].astype('float')
        return df
    except Exception as e:
        raise ffpException(e, sys)
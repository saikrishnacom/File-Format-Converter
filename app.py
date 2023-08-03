import json
import uuid
import os
import glob
import pandas as pd
import logging


def get_columns(ds):
    schemas_file_path = os.environ.setdefault('SCHEMAS_FILE_PATH','data/retail_db/schemas.json')

    with open(schemas_file_path) as fp:
        schemas = json.load(fp)
    try:
        schema = schemas.get(ds)
        if not schema:
            raise KeyError
        cols = sorted(schema,key=lambda s:s['column_position'])
        column = [col['column_name'] for col in cols]
        return column
    except KeyError:
        logging.error(f'schemas not found for{ds}')
        raise
def process_file(src_base_dir,ds,tgt_base_dir):
    for file in glob.glob(f'{src_base_dir}/{ds}/*'):
        try:
            df= pd.read_csv(file,names=get_columns(ds))
            os.makedirs(f'{tgt_base_dir}/{ds}',exist_ok=True)
            df.to_json(f'{tgt_base_dir}/{ds}/part-{str(uuid.uuid1())}.json',
                            orient='records',
                            lines=True)
            logging.info(f'number of records processed  for {os.path.split(file)[1]} in {ds} is {df.shape[0]}')
        except KeyError:
            raise

def main():
    logging.basicConfig(
         filename='logs/ffc.log',
         level=logging.INFO,
         format='%(levelname)s %(asctime)s %(message)s',
         datefmt='%Y-%m-%d %I:%M:%S %p'
    )
    src_base_dir = os.environ['SRC_BASE_DIR']
    tgt_base_dir = os.environ['TGT_BASE_DIR']
    datasets = os.environ.get('DATASETS')
    logging.info('file format conversion:started')
    if not datasets:
        for path in glob.glob(f'{src_base_dir}/*'):
            if os.path.isdir(path):
                process_file(src_base_dir,os.path.split(path)[1],tgt_base_dir)
    else:
         dirs = datasets.split(',')
         for ds in dirs:
             try:
                process_file(src_base_dir,ds,tgt_base_dir)
             except Exception as e:
                logging.info(f'file format conversion of{ds} is not sucesseful')
    logging.info('file format conversion:succesful')

if __name__=="__main__": 
    main()


#!/usr/bin/python3
import logging
import os
from typing import List, Union
from google.cloud import aiplatform
from dotenv import load_dotenv

load_dotenv()

def create_and_import_dataset_image_sample(
    project: str,
    location: str,
    display_name: str,
    src_uris: Union[str, List[str]],
    sync: bool = True,
):
    """
    src_uris -- a string or list of strings, e.g.
        ["gs://bucket1/source1.jsonl", "gs://bucket7/source4.jsonl"]
    """

    aiplatform.init(project=project, location=location)

    ds = aiplatform.ImageDataset.create(
        display_name=display_name,
        gcs_source=src_uris,
        import_schema_uri=aiplatform.schema.dataset.ioformat.image.multi_label_classification,
        sync=sync,
    )

    ds.wait()

    logging.info(ds.display_name)
    logging.info(ds.resource_name)
    return ds


PROJECT = os.getenv('PROJECT')
LOCATION = os.getenv('LOCATION')
JSONL_URI = os.getenv('JSONL_URI')

dataset = create_and_import_dataset_image_sample(PROJECT, LOCATION, PROJECT, JSONL_URI, False)
import logging
import os

import azure.functions as func
import requests
from azure.storage.blob import BlobServiceClient


def main(mytimer: func.TimerRequest) -> None:
    try:
        blob_service_client = BlobServiceClient.from_connection_string(
            os.environ["AZURERBAC_STORAGE_ACCOUNT_CONNECTION_STRING"]
        )
        blob_client = blob_service_client.get_blob_client(
            "rbacreport", "rbac_report.csv"
        )
        payload = blob_client.download_blob().content_as_text(encoding="UTF-8")
        logging.info(
            requests.post(
                json={"attachment": payload}, url=os.environ["AZURERBAC_LOGICAPP_URL"]
            )
        )

    except Exception as e:
        logging.info(str(e))
    logging.info("-----------------------------------------------------------")
    logging.info(f"******* Completed sending the attachment *******")

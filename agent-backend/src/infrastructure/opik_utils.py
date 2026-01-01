import os

import opik
import logging
from opik.configurator.configure import OpikConfigurator
from opik.rest_api.core.api_error import ApiError

from src.config import settings


def configure() -> None:
    if settings.COMET_API_KEY and settings.COMET_PROJECT:
        try:
            client = OpikConfigurator(api_key=settings.COMET_API_KEY)
            default_workspace = client._get_default_workspace()
        except Exception:
            logging.warning(
                "Default workspace not found. Setting workspace to None and enabling interactive mode."
            )
            default_workspace = None

        os.environ["OPIK_PROJECT_NAME"] = settings.COMET_PROJECT

        try:
            opik.configure(
                api_key=settings.COMET_API_KEY,
                workspace=default_workspace,
                use_local=False,
                force=True,
            )
            logging.info(
                f"Opik configured successfully using workspace '{default_workspace}'"
            )
        except Exception:
            logging.warning(
                "Couldn't configure Opik. There is probably a problem with the COMET_API_KEY or COMET_PROJECT environment variables or with the Opik server."
            )
    else:
        logging.warning(
            "COMET_API_KEY and COMET_PROJECT are not set. Set them to enable prompt monitoring with Opik (powered by Comet ML)."
        )

def get_dataset(name: str) -> opik.Dataset | None:
    client = opik.Opik()
    try:
        dataset = client.get_dataset(name=name)
    except Exception:
        dataset = None

    return dataset


def create_dataset(name: str, description: str, items: list[dict]) -> opik.Dataset:
    client = opik.Opik()
    
    try:
        client.get_dataset(name=name)
        # If we reach here, dataset exists
        client.delete_dataset(name=name)

    except ApiError as e:
        if e.status_code == 404:
            # Dataset does not exist → safe to create
            pass
        else:
            raise

    dataset = client.create_dataset(name=name, description=description)
    dataset.insert(items)

    return dataset

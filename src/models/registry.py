import mlflow
from src.config import settings
from src.utils.logging import logger

class ModelRegistry:
    def __init__(self, tracking_uri: str = settings.MLFLOW_TRACKING_URI):
        mlflow.set_tracking_uri(tracking_uri)

    def register_model(self, model, artifact_path: str, name: str):
        with mlflow.start_run() as run:
            mlflow.pytorch.log_model(model, artifact_path=artifact_path, registered_model_name=name)
            logger.info(f"Model {name} registered with run_id {run.info.run_id}")

    def load_model(self, name: str, stage: str = "Production"):
        model_uri = f"models:/{name}/{stage}"
        model = mlflow.pytorch.load_model(model_uri)
        logger.info(f"Loaded model {name} from stage {stage}")
        return model

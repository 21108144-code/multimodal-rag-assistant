import argparse
import mlflow
import torch
from src.config import settings
from src.utils.logging import logger

def train(epochs: int = 1, learning_rate: float = 1e-4):
    logger.info("Starting training...")
    mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
    mlflow.set_experiment("multimodal-rag-finetuning")

    with mlflow.start_run():
        mlflow.log_param("epochs", epochs)
        mlflow.log_param("learning_rate", learning_rate)

        # Placeholder for training loop
        # model = ...
        # optimizer = ...
        # for epoch in range(epochs):
        #     loss = ...
        #     mlflow.log_metric("loss", loss)
        
        logger.info("Training completed (mock).")
        # mlflow.pytorch.log_model(model, "model")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=1)
    parser.add_argument("--lr", type=float, default=1e-4)
    args = parser.parse_args()
    train(args.epochs, args.lr)

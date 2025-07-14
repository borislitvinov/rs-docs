"""AWS Lambda entry point for Slack bot."""

import logging
from .lambda_handler import LambdaHandler

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize the handler once per container
lambda_handler_instance = LambdaHandler()


def lambda_handler(event, context):
    """AWS Lambda entry point function."""
    return lambda_handler_instance.handle_request(event, context)

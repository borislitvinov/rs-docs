"""Main Lambda handler orchestrator."""

import json
import logging
from typing import Dict, Any
from slack_sdk import WebClient

from .token_manager import TokenManager
from .slack_event_processor import SlackEventProcessor
from .response_builder import ResponseBuilder


class LambdaHandler:
    """Main orchestrator for AWS Lambda Slack bot."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.token_manager = TokenManager()
        self.slack_client = None
        self.event_processor = None
        
        # Initialize Slack client if token is available
        if self.token_manager.is_token_available():
            self.slack_client = WebClient(token=self.token_manager.token)
            self.event_processor = SlackEventProcessor(self.slack_client)
        else:
            self.logger.error("Cannot initialize Slack client: no valid token available")
    
    def handle_request(self, event: Dict[str, Any], context: Any) -> Dict[str, Any]:
        """Handle incoming Lambda request."""
        try:
            self.logger.info(f"Received event: {json.dumps(event)}")
            
            # Check if Slack client is available
            if not self.slack_client or not self.event_processor:
                self.logger.error("Slack client not initialized")
                return ResponseBuilder.internal_error("Service unavailable")
            
            # Parse the event body
            event_body = self._parse_event_body(event)
            if event_body is None:
                return ResponseBuilder.bad_request("Invalid JSON in request body")
            
            # Process the event
            response = self.event_processor.process_event(event_body)
            
            self.logger.info("Finished processing event, returning response")
            return response
            
        except Exception as e:
            self.logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
            return ResponseBuilder.internal_error(str(e))
    
    def _parse_event_body(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Parse the event body from Lambda event."""
        # Handle both direct Lambda invocation and API Gateway events
        if 'body' in event:
            try:
                body = json.loads(event['body'])
                self.logger.info(f"Parsed body from API Gateway: {json.dumps(body)}")
                return body
            except json.JSONDecodeError as e:
                self.logger.error(f"Error parsing body: {e}")
                return None
        else:
            # Direct Lambda invocation
            self.logger.info(f"Using event as body (direct invocation): {json.dumps(event)}")
            return event

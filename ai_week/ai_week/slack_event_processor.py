"""Slack event processing logic."""

import json
import logging
from typing import Dict, Any, Optional
from slack_sdk import WebClient

from .slack_message_handler import SlackMessageHandler
from .response_builder import ResponseBuilder


class SlackEventProcessor:
    """Processes different types of Slack events."""
    
    def __init__(self, slack_client: WebClient):
        self.slack_client = slack_client
        self.message_handler = SlackMessageHandler(slack_client)
        self.logger = logging.getLogger(__name__)
    
    def process_event(self, event_body: Dict[str, Any]) -> Dict[str, Any]:
        """Process a Slack event and return appropriate response."""
        self.logger.info(f"Processing event body: {json.dumps(event_body)}")
        
        # Handle Slack URL verification challenge
        if event_body.get('type') == 'url_verification':
            return self._handle_url_verification(event_body)
        
        # Handle event callbacks
        if event_body.get('type') == 'event_callback' and 'event' in event_body:
            return self._handle_event_callback(event_body)
        
        # Unknown event type
        self.logger.warning(f"Unknown event type: {event_body.get('type')}")
        return ResponseBuilder.success("Event processed")
    
    def _handle_url_verification(self, event_body: Dict[str, Any]) -> Dict[str, Any]:
        """Handle Slack URL verification challenge."""
        self.logger.info("Handling URL verification challenge")
        challenge = event_body.get('challenge')
        
        if not challenge:
            self.logger.error("No challenge found in URL verification request")
            return ResponseBuilder.bad_request("Missing challenge parameter")
        
        return ResponseBuilder.slack_challenge_response(challenge)
    
    def _handle_event_callback(self, event_body: Dict[str, Any]) -> Dict[str, Any]:
        """Handle Slack event callback."""
        slack_event = event_body['event']
        event_type = slack_event.get('type')
        
        self.logger.info(f"Processing Slack event: {event_type}")
        
        if event_type == 'message':
            return self._handle_message_event(slack_event)
        
        # Handle other event types here in the future
        self.logger.info(f"Event type '{event_type}' not handled, returning success")
        return ResponseBuilder.success("Event processed")
    
    def _handle_message_event(self, message_event: Dict[str, Any]) -> Dict[str, Any]:
        """Handle a Slack message event."""
        channel = message_event.get('channel')
        self.logger.info(f"Message event in channel: {channel}")
        
        # Process the message
        success = self.message_handler.process_message(message_event)
        
        if success:
            return ResponseBuilder.success("Message processed")
        else:
            self.logger.error("Failed to process message")
            return ResponseBuilder.success("Message processing failed, but returning success to avoid retries")

"""Slack message handling logic."""

import logging
import os
from typing import Dict, Any, Optional
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class SlackMessageHandler:
    """Handles Slack message processing and responses."""
    
    def __init__(self, slack_client: WebClient):
        self.slack_client = slack_client
        self.logger = logging.getLogger(__name__)
    
    def should_process_message(self, message_event: Dict[str, Any]) -> bool:
        """Determine if a message should be processed."""
        # Skip bot messages to avoid loops
        if message_event.get('bot_id') or message_event.get('subtype') == 'bot_message':
            self.logger.info("Skipping bot message")
            return False
        
        # Skip messages that contain our own mention pattern to avoid loops
        message_text = message_event.get('text', '')
        if "<@U091507G726> provide the answer:" in message_text:
            self.logger.info("Skipping message containing our own mention pattern")
            return False

        return True
    
    def process_message(self, message_event: Dict[str, Any]) -> bool:
        """Process a Slack message event."""
        if not self.should_process_message(message_event):
            return True  # Successfully skipped
        
        channel = message_event.get('channel')
        message_text = message_event.get('text', '')
        thread_ts = message_event.get('ts')
        
        self.logger.info(f"Processing message in channel {channel}: {message_text}")
        
        try:
            response_text = self._generate_response(message_text)
            return self._send_response(channel, response_text, thread_ts)
            
        except Exception as e:
            self.logger.error(f"Error processing message: {str(e)}")
            return False
    
    def _generate_response(self, message_text: str) -> str:
        """Generate a response to the message."""
        # For now, we'll use the existing logic
        return f"<@U091507G726> provide the answer: {message_text}"
    
    def _send_response(self, channel: str, response_text: str, thread_ts: Optional[str] = None) -> bool:
        """Send a response message to Slack."""
        try:
            self.logger.info("Attempting to send message via Slack SDK")
            
            response = self.slack_client.chat_postMessage(
                channel=channel,
                text=response_text,
                thread_ts=thread_ts  # Reply in thread if provided
            )
            
            self.logger.info(f"Message sent successfully: {response}")
            return True
            
        except SlackApiError as e:
            self.logger.error(f"Error posting message: {e}")
            self.logger.error(f"Error details: {e.response['error']}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error sending message: {str(e)}")
            return False

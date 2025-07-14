"""HTTP response builder for AWS Lambda."""

import json
from typing import Dict, Any, Optional


class ResponseBuilder:
    """Builds standardized HTTP responses for AWS Lambda."""
    
    @staticmethod
    def success(message: str = "ok", data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Build a successful HTTP response."""
        body = {"status": message}
        if data:
            body.update(data)
        
        return {
            'statusCode': 200,
            'body': json.dumps(body)
        }
    
    @staticmethod
    def bad_request(error_message: str) -> Dict[str, Any]:
        """Build a bad request HTTP response."""
        return {
            'statusCode': 400,
            'body': json.dumps({'error': error_message})
        }
    
    @staticmethod
    def internal_error(error_message: str) -> Dict[str, Any]:
        """Build an internal server error HTTP response."""
        return {
            'statusCode': 500,
            'body': json.dumps({'error': error_message})
        }
    
    @staticmethod
    def slack_challenge_response(challenge: str) -> Dict[str, Any]:
        """Build a response for Slack URL verification challenge."""
        return {
            'statusCode': 200,
            'body': json.dumps({'challenge': challenge})
        }

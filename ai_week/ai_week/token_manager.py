"""Token management for AWS Lambda Slack bot."""

import os
import logging
import boto3
from base64 import b64decode
from typing import Optional


class TokenManager:
    """Manages Slack bot token decryption and retrieval."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._token: Optional[str] = None
        self._initialize_token()
    
    def _initialize_token(self) -> None:
        """Initialize and decrypt the Slack bot token."""
        encrypted_token = os.environ.get('SLACK_BOT_TOKEN')
        
        if not encrypted_token:
            self.logger.error("SLACK_BOT_TOKEN environment variable not found")
            self._token = None
            return
        
        try:
            # Check if the token appears to be encrypted (typically starts with AQI for KMS encrypted values)
            if encrypted_token.startswith('AQI'):
                self.logger.info("Token appears to be encrypted, attempting to decrypt")
                self._token = self._decrypt_token(encrypted_token)
            else:
                self.logger.info("Token does not appear to be encrypted, using as-is")
                self._token = encrypted_token
                
        except Exception as e:
            self.logger.error(f"Error processing token: {str(e)}")
            self._token = encrypted_token  # Fallback to encrypted value
        
        # Log token status (first 5 characters only for security)
        token_preview = self._token[:5] if self._token else 'None'
        self.logger.info(f"Token initialized: {token_preview}...")
    
    def _decrypt_token(self, encrypted_token: str) -> str:
        """Decrypt KMS-encrypted token."""
        try:
            kms_client = boto3.client('kms')
            
            # Get the Lambda function name for encryption context
            function_name = os.environ.get('AWS_LAMBDA_FUNCTION_NAME')
            if not function_name:
                raise ValueError("AWS_LAMBDA_FUNCTION_NAME environment variable not found")
            
            # Decrypt the token
            response = kms_client.decrypt(
                CiphertextBlob=b64decode(encrypted_token),
                EncryptionContext={'LambdaFunctionName': function_name}
            )
            
            decrypted_token = response['Plaintext'].decode('utf-8')
            self.logger.info("Token successfully decrypted")
            return decrypted_token
            
        except Exception as e:
            self.logger.error(f"Failed to decrypt token: {str(e)}")
            raise
    
    @property
    def token(self) -> Optional[str]:
        """Get the decrypted Slack bot token."""
        return self._token
    
    def is_token_available(self) -> bool:
        """Check if a valid token is available."""
        return self._token is not None and len(self._token) > 0

import logging
import time
from google.api_core.exceptions import GoogleAPIError
import vertexai
# This import is new and correct for Gemini
from vertexai.generative_models import GenerativeModel, ChatSession
from typing import Optional

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class GeminiClient:
    def __init__(
        self,
        project_id: str,
        location: str = "us-central1",
        model_name: str = "models/gemini-1.5-flash-latest",
        system_instruction: Optional[str] = None
    ):
        """
        Initializes the Vertex AI generative client for Gemini.
        """
        vertexai.init(project=project_id, location=location)
        # Load the specified Gemini model
        self.model = GenerativeModel(
            model_name=model_name,
            system_instruction=[system_instruction] if system_instruction else None
        )
        self.chat_session = self.model.start_chat()

    def send_message(
        self,
        message: str,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ) -> str:
        """
        Sends a message to the chat model and returns the response.
        """
        attempt = 0
        while attempt < max_retries:
            try:
                # Use the existing chat session to send a message
                response = self.chat_session.send_message(message)
                return response.text

            except GoogleAPIError as e:
                attempt += 1
                logger.warning(
                    f"Retry {attempt}/{max_retries} after error: {e}"
                )
                time.sleep(retry_delay)

        raise RuntimeError("Failed to get response after retries.")
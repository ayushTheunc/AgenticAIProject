from pydantic import BaseModel


class ChatMessageResponse(BaseModel):
    chat_id: int
    user_prompt: str
    api_response: str
    session_id: int

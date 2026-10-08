from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    openai_model: str
    openai_temperature: float
    openai_timeout: int
    host: str
    port: int
    memory_file: str
    max_messages: int
    system_prompt_file: str

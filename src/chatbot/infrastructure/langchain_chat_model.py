from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from ..domain.errors import UpstreamError
from ..domain.ports.chat_model import ChatModel
from .map_openai_error import map_openai_error

LOI_RONG = "Mô hình trả về câu trả lời rỗng."


class LangChainChatModel(ChatModel):
    """Cầu nối tới mô hình trả lời, đọc khóa API ở mỗi lượt gọi."""

    def __init__(self, settings, store):
        self._settings = settings
        self._store = store

    def reply(self, system_prompt, history, user_text):
        mau = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder("history"),
            ("human", "{input}"),
        ])
        mo_hinh = ChatOpenAI(
            model=self._settings.openai_model,
            temperature=self._settings.openai_temperature,
            timeout=self._settings.openai_timeout,
            api_key=self._store.get(),
        )
        try:
            ket_qua = mo_hinh.invoke(mau.invoke({
                "history": self._doi_doi(history),
                "input": user_text,
            }))
        except Exception as loi:
            ma, thong_diep = map_openai_error(loi)
            raise UpstreamError(ma, thong_diep) from loi
        noi_dung = (ket_qua.content or "").strip()
        if not noi_dung:
            raise UpstreamError(502, LOI_RONG)
        return noi_dung

    def _doi_doi(self, history):
        doi = []
        for tin in history:
            if tin.role == "human":
                doi.append(HumanMessage(content=tin.content))
            else:
                doi.append(AIMessage(content=tin.content))
        return doi

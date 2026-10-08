import openai

THONG_DIEP = {
    401: "Khóa API không đúng, nhập lại.",
    503: "Hệ thống đang quá tải, thử lại sau.",
    504: "Mô hình trả lời quá lâu.",
    502: "Không kết nối được dịch vụ mô hình.",
    500: "Có lỗi không mong đợi.",
}


def map_openai_error(exc):
    """Dịch lỗi OpenAI thành cặp (mã trạng thái, thông điệp tiếng Việt)."""
    if isinstance(exc, openai.AuthenticationError):
        ma = 401
    elif isinstance(exc, openai.RateLimitError):
        ma = 503
    elif isinstance(exc, openai.APITimeoutError):
        ma = 504
    elif isinstance(exc, openai.APIConnectionError):
        ma = 502
    else:
        ma = 500
    return ma, THONG_DIEP[ma]

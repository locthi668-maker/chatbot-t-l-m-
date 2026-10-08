import os
import tempfile
from pathlib import Path


def atomic_write_text(path, text):
    """Ghi văn bản theo kiểu nguyên tử: ghi tệp tạm cùng thư mục rồi os.replace."""
    dich = Path(path)
    dich.parent.mkdir(parents=True, exist_ok=True)
    mo_ta, ten_tam = tempfile.mkstemp(prefix=dich.name + ".tmp-", dir=str(dich.parent))
    duong_dan_tam = Path(ten_tam)
    try:
        with os.fdopen(mo_ta, "w", encoding="utf-8", newline="") as tep:
            tep.write(text)
            tep.flush()
            os.fsync(tep.fileno())
        os.replace(duong_dan_tam, dich)
    except BaseException:
        duong_dan_tam.unlink(missing_ok=True)
        raise
    return str(dich)

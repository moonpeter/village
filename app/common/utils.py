import os
from uuid import uuid4
import datetime


def rename_imagefile_to_uuid(instance, filename):
    dt_today = datetime.date.today()
    upload_to = f"posts/{dt_today.strftime('%Y')}/{dt_today.strftime('%m')}/{dt_today.strftime('%d')}"
    ext = filename.split(".")[-1]
    filename_text = filename.split(".")[0]
    uuid = uuid4().hex

    filename = f"{uuid}_{filename_text}.{ext}"

    return os.path.join(upload_to, filename)


def rename_imagefile_to_uuid_for_comment(instance, filename):
    dt_today = datetime.date.today()
    upload_to = f"comments/{dt_today.strftime('%Y')}/{dt_today.strftime('%m')}/{dt_today.strftime('%d')}"
    ext = filename.split(".")[-1]
    filename_text = filename.split(".")[0]
    uuid = uuid4().hex

    filename = f"{uuid}_{filename_text}.{ext}"

    return os.path.join(upload_to, filename)


mbti_itmes = [
    # 분석형
    ("INTJ", "INTJ"),
    ("INTP", "INTP"),
    ("ENTJ", "ENTJ"),
    ("ENTP", "ENTP"),
    # 외교형
    ("INFJ", "INFJ"),
    ("INFP", "INFP"),
    ("ENFJ", "ENFJ"),
    ("ENFP", "ENFP"),
    # 관리형
    ("ISTJ", "ISTJ"),
    ("ISFJ", "ISFJ"),
    ("ESTJ", "ESTJ"),
    ("ESFJ", "ESFJ"),
    # 탐험가형
    ("ISTP", "ISTP"),
    ("ISFP", "ISFP"),
    ("ESTP", "ESTP"),
    ("ESFP", "ESFP"),
]
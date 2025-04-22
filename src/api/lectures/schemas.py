from datetime import datetime
from pydantic import BaseModel


class LectureMetadata(BaseModel):
    title: str
    type: str
    visibility: str
    user_id: str

class VideoLectureMetadata(LectureMetadata):
    video_s3_key: str

class TextLectureMetadata(LectureMetadata):
    content: str

class VideoLectureReadMetadata(VideoLectureMetadata):
    id: str
    processing_status: str
    created_at: datetime
    updated_at: datetime


class TextLectureReadMetadata(VideoLectureMetadata):
    id: str
    created_at: datetime
    updated_at: datetime

class LectureReadData(LectureMetadata):
    id: str
    created_at: datetime
    updated_at: datetime

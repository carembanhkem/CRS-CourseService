from abc import ABC
import uuid

from sqlmodel import Session, select

from api.db.constants import LectureType, ProcessingStatus
from api.db.models import LectureModel


class LectureService(ABC):

    def create_new_lecture(self, session: Session, **kargs):
        pass
    
    def get_all_lectures(self, session: Session):
        pass

class VideoLectureService(LectureService):
    def create_new_lecture(self, session: Session, **kwargs):
        if kwargs["type"] == "VIDEO":
            processing_status = "IN_PROGRESS"
        else:
            processing_status = "COMPLETED"
        video_lecture = LectureModel(
            title=kwargs["title"],
            type=kwargs["type"],
            video_s3_key=kwargs["video_s3_key"],
            visibility=kwargs["visibility"],
            user_id=kwargs["user_id"],
            processing_status=processing_status,
        )
        session.add(video_lecture)
        session.commit()
        session.refresh(video_lecture)

        return video_lecture

    def get_all_lectures(self, session: Session):
        query = select(LectureModel).where(
            (LectureModel.type == LectureType.VIDEO) 
            # & (LectureModel.processing_status == ProcessingStatus.COMPLETED)
        )
        result = session.exec(query).all()
        return result

    def get_lectures_by_user_id(self, user_id: str, session: Session):
        query = select(LectureModel).where(
            (LectureModel.type == LectureType.VIDEO)
            # & (LectureModel.processing_status == ProcessingStatus.COMPLETED)
            & (LectureModel.user_id == user_id)
        )
        result = session.exec(query).all()
        return result

    def get_lecture_by_id(self, video_s3_key: str, session: Session):
        query = select(LectureModel).where(
            (LectureModel.type == LectureType.VIDEO)
            # & (LectureModel.processing_status == ProcessingStatus.COMPLETED)
            & (LectureModel.video_s3_key == video_s3_key)
        )
        result = session.exec(query).first()
        return result

class TextLectureService(LectureService):
    def create_new_lecture(self, session: Session, **kwargs):
        pass

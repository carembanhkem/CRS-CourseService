import boto3
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from api.db.middleware.auth_middleware import get_current_user
from api.db.session import get_session
from api.lectures.schemas import TextLectureMetadata, TextLectureReadMetadata, VideoLectureMetadata, VideoLectureReadMetadata
from api.lectures.service import TextLectureService, VideoLectureService
from secret_keys import SecretKeys


lecture_router = APIRouter()
secret_keys = SecretKeys()

s3_client = boto3.client("s3", region_name=secret_keys.AWS_REGION)

@lecture_router.get("/url")
def get_presigned_url(user=Depends(get_current_user)):
    try:
        video_id = f"videos/{user['sub']}/{uuid.uuid4()}"  # we already set prefix of objects stored in S3 bucket is "videos".
        # The uuid part make the video_id is unique
        # print(video_id)

        response = s3_client.generate_presigned_url(
            "put_object", # type of request
            Params={ # Object information about to be uploaded
                "Bucket": secret_keys.AWS_RAW_VIDEOS_BUCKET,
                "Key": video_id,
                "ContentType": "video/mp4"
            }
        )
        # print(response)

        return {
            'url': response,
            'video_id': video_id
        }
    except Exception as e:
        raise HTTPException(500, str(e))


@lecture_router.post(
    "/metadata", response_model=VideoLectureReadMetadata | TextLectureReadMetadata
)
def upload_metadata(
    metadata: VideoLectureMetadata | TextLectureMetadata,
    user=Depends(get_current_user),
    session: Session = Depends(get_session),
):
    if metadata.type == "VIDEO":
        service = VideoLectureService()
    elif metadata.type == "TEXT":
        service = TextLectureService()

    new_lecture = service.create_new_lecture(session, **metadata.model_dump())

    if not new_lecture:
        raise HTTPException(400, "Fail to create Lecture")

    return new_lecture.model_dump(mode="json")

@lecture_router.get("/")
def get_all_lectures(user=Depends(get_current_user),
    session: Session = Depends(get_session),):
    service = TextLectureService()
    pass
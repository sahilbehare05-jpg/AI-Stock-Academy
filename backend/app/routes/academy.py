from datetime import datetime, timezone
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException
from fastapi import APIRouter, Depends
from app.database.db import get_database, Collections
from app.utils.deps import get_current_user


router = APIRouter(
    prefix="/api/academy",
    tags=["Trading Academy"],
)


@router.get("/modules")
async def get_modules(
    current_user: dict = Depends(get_current_user),
):
    db = get_database()

    modules = await db[Collections.MODULES].find(
        {}
    ).sort("order", 1).to_list(length=None)

    result = []

    for module in modules:
        result.append({
            "id": str(module["_id"]),
            "title": module.get("title", ""),
            "description": module.get("description", ""),
            "level": module.get("level", "Beginner"),
            "order": module.get("order", 0),
            "lesson_count": module.get("lesson_count", 0),
        })

    return {
        "success": True,
        "data": result,
    }
@router.get("/modules/{module_id}/lessons")
async def get_module_lessons(
    module_id: str,
    current_user: dict = Depends(get_current_user),
):
    try:
        module_object_id = ObjectId(module_id)
    except InvalidId:
        raise HTTPException(
            status_code=400,
            detail="Invalid module ID.",
        )

    db = get_database()

    module = await db[Collections.MODULES].find_one(
        {"_id": module_object_id}
    )

    if not module:
        raise HTTPException(
            status_code=404,
            detail="Module not found.",
        )

    lessons = await db[Collections.LESSONS].find(
        {"module_id": module_object_id}
    ).sort("lesson_order", 1).to_list(length=None)

    result = []

    for lesson in lessons:
        result.append({
            "id": str(lesson["_id"]),
            "module_id": str(lesson["module_id"]),
            "lesson_order": lesson.get("lesson_order", 0),
            "title": lesson.get("title", ""),
            "level": lesson.get("level", "Beginner"),
            "estimated_minutes": lesson.get(
                "estimated_minutes", 0
            ),
            "content": lesson.get("content", {}),
        })

    return {
        "success": True,
        "data": {
            "module": {
                "id": str(module["_id"]),
                "title": module.get("title", ""),
                "description": module.get(
                    "description", ""
                ),
                "level": module.get(
                    "level", "Beginner"
                ),
            },
            "lessons": result,
        },
    }
@router.post("/lessons/{lesson_id}/complete")
async def complete_lesson(
    lesson_id: str,
    current_user: dict = Depends(get_current_user),
):
    try:
        lesson_object_id = ObjectId(lesson_id)
    except InvalidId:
        raise HTTPException(
            status_code=400,
            detail="Invalid lesson ID.",
        )

    db = get_database()

    lesson = await db[Collections.LESSONS].find_one(
        {"_id": lesson_object_id}
    )

    if not lesson:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found.",
        )

    user_id = ObjectId(current_user["id"])

    existing = await db[Collections.TRAINING_PROGRESS].find_one(
        {
            "user_id": user_id,
            "lesson_id": lesson_object_id,
        }
    )

    if existing:
        return {
            "success": True,
            "data": {
                "message": "Lesson already completed.",
                "completed": True,
                "lesson_id": lesson_id,
            },
        }

    await db[Collections.TRAINING_PROGRESS].insert_one(
        {
            "user_id": user_id,
            "lesson_id": lesson_object_id,
            "module_id": lesson["module_id"],
            "completed": True,
            "completed_at": datetime.now(timezone.utc),
        }
    )

    return {
        "success": True,
        "data": {
            "message": "Lesson completed successfully.",
            "completed": True,
            "lesson_id": lesson_id,
        },
    }
@router.get("/progress")
async def get_academy_progress(
    current_user: dict = Depends(get_current_user),
):
    db = get_database()

    user_id = ObjectId(current_user["id"])

    completed_lessons = await db[
        Collections.TRAINING_PROGRESS
    ].find(
        {
            "user_id": user_id,
            "completed": True,
        }
    ).to_list(length=None)

    completed_lesson_ids = {
        item["lesson_id"]
        for item in completed_lessons
    }

    total_lessons = await db[
        Collections.LESSONS
    ].count_documents({})

    completed_count = len(completed_lesson_ids)

    progress_percent = (
        round((completed_count / total_lessons) * 100, 2)
        if total_lessons > 0
        else 0
    )

    score = round(
        (completed_count / total_lessons) * 10000
    ) if total_lessons > 0 else 0

    return {
        "success": True,
        "data": {
            "total_lessons": total_lessons,
            "completed_lessons": completed_count,
            "progress_percent": progress_percent,
            "score": score,
            "max_score": 10000,
        },
    }
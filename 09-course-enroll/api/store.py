"""In-memory course enrollment store."""

from __future__ import annotations

from copy import deepcopy

_courses: dict[str, dict] = {}
_enrollments: dict[str, dict] = {}


def reset() -> None:
    global _courses, _enrollments
    _courses = {
        "c1": {"id": "c1", "title": "Intro to Python"},
        "c2": {"id": "c2", "title": "Data Structures"},
    }
    _enrollments = {
        "en1": {"id": "en1", "course_id": "c1", "student_id": "alice"},
    }


def list_courses(search: str | None = None) -> list[dict]:
    courses = list(_courses.values())
    if not search:
        return deepcopy(courses)
    return deepcopy([c for c in courses if c["title"] == search])


def get_course(course_id: str) -> dict | None:
    course = _courses.get(course_id)
    return deepcopy(course) if course else None


def create_course(title: str) -> dict:
    course_id = f"c{len(_courses) + 1}"
    course = {"id": course_id, "title": title}
    _courses[course_id] = course
    return deepcopy(course)


def list_enrollments(course_id: str) -> list[dict] | None:
    if course_id not in _courses:
        return None
    return deepcopy([e for e in _enrollments.values() if e["course_id"] == course_id])


def enroll_student(course_id: str, student_id: str) -> dict:
    enrollment_id = f"en{len(_enrollments) + 1}"
    enrollment = {"id": enrollment_id, "course_id": course_id, "student_id": student_id}
    _enrollments[enrollment_id] = enrollment
    return deepcopy(enrollment)


def delete_enrollment(enrollment_id: str) -> bool:
    if enrollment_id not in _enrollments:
        return False
    del _enrollments[enrollment_id]
    return True


reset()

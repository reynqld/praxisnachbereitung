from datetime import datetime, timezone

import psycopg
from fastapi import APIRouter, HTTPException, status

from .db import get_conn
from .models import AssignmentCreate, AssignmentReturn, DeviceCreate


router = APIRouter()


def parse_datetime(value: str | None) -> datetime:
    if value is None:
        return datetime.now(timezone.utc)

    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Ungültiger Zeitpunkt",
        ) from exc

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)

    return parsed


@router.get("/devices")
def get_devices():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, serial_number, device_type_id, location_id
            FROM device
            ORDER BY id
            """
        )
        return cur.fetchall()


@router.post("/devices", status_code=status.HTTP_201_CREATED)
def create_device(device: DeviceCreate):
    try:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO device (serial_number, device_type_id, location_id)
                VALUES (%s, %s, %s)
                RETURNING id, serial_number, device_type_id, location_id
                """,
                (device.serial_number, device.device_type_id, device.location_id),
            )
            return cur.fetchone()
    except psycopg.errors.UniqueViolation as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Die Seriennummer existiert bereits",
        ) from exc


@router.get("/assignments/active")
def get_active_assignments():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, device_id, person_id, issued_at, returned_at
            FROM assignment
            WHERE returned_at IS NULL
            ORDER BY id
            """
        )
        return cur.fetchall()


@router.post("/assignments", status_code=status.HTTP_201_CREATED)
def create_assignment(assignment: AssignmentCreate):
    issued_at = parse_datetime(assignment.issued_at)

    try:
        with get_conn() as conn, conn.transaction(), conn.cursor() as cur:
            cur.execute(
                "SELECT id FROM device WHERE id = %s FOR UPDATE",
                (assignment.device_id,),
            )
            if cur.fetchone() is None:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Das Device existiert nicht",
                )

            cur.execute(
                """
                SELECT id
                FROM assignment
                WHERE device_id = %s AND returned_at IS NULL
                """,
                (assignment.device_id,),
            )
            if cur.fetchone() is not None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Das Device hat bereits eine aktive Ausleihe",
                )

            cur.execute(
                """
                INSERT INTO assignment (device_id, person_id, issued_at)
                VALUES (%s, %s, %s)
                RETURNING id, device_id, person_id, issued_at, returned_at
                """,
                (assignment.device_id, assignment.person_id, issued_at),
            )
            return cur.fetchone()
    except psycopg.errors.ForeignKeyViolation as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Die Person existiert nicht",
        ) from exc


@router.post("/assignments/{assignment_id}/return")
def return_assignment(assignment_id: int, assignment_return: AssignmentReturn):
    returned_at = parse_datetime(assignment_return.returned_at)

    with get_conn() as conn, conn.transaction(), conn.cursor() as cur:
        cur.execute(
            """
            SELECT issued_at
            FROM assignment
            WHERE id = %s
            FOR UPDATE
            """,
            (assignment_id,),
        )
        assignment = cur.fetchone()

        if assignment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Die Ausleihe existiert nicht",
            )

        if returned_at < assignment["issued_at"]:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="returned_at darf nicht vor issued_at liegen",
            )

        cur.execute(
            """
            UPDATE assignment
            SET returned_at = %s
            WHERE id = %s
            RETURNING id, device_id, person_id, issued_at, returned_at
            """,
            (returned_at, assignment_id),
        )
        return cur.fetchone()

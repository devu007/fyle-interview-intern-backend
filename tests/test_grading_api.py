# tests/test_grading_api.py

import pytest
from flask import url_for
from core.models.assignments import Assignment, GradeEnum
from core import db

def test_teacher_grades_assignment(client, h_teacher_1, setup_assignments):
    assignment = setup_assignments[0]
    response = client.post(
        url_for('teacher_assignments_resources.grade_assignment'),
        headers=h_teacher_1,
        json={"id": assignment.id, "grade": "A"}
    )
    assert response.status_code == 200
    assert response.json['data']['grade'] == "A"

def test_principal_regrades_assignment(client, h_principal, setup_assignments):
    assignment = setup_assignments[0]
    assignment.grade = GradeEnum.A
    db.session.commit()

    response = client.post(
        url_for('principal_assignments_resources.grade_assignment'),
        headers=h_principal,
        json={"id": assignment.id, "grade": "B"}
    )
    assert response.status_code == 200
    assert response.json['data']['grade'] == "B"

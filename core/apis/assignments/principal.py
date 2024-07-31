from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.teachers import Teacher  # Assuming you have a Teacher model
from .schema import AssignmentSchema, AssignmentGradeSchema, TeacherSchema  # Ensure TeacherSchema is defined

principal_resources = Blueprint('principal_resources', __name__)

@principal_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_all_assignments(p):
    """Returns list of all submitted and graded assignments"""
    all_assignments = Assignment.query.filter(Assignment.state.in_(['SUBMITTED', 'GRADED'])).all()
    all_assignments_dump = AssignmentSchema().dump(all_assignments, many=True)
    return APIResponse.respond(data=all_assignments_dump)

@principal_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_all_teachers(p):
    """Returns list of all teachers"""
    all_teachers = Teacher.query.all()
    all_teachers_dump = TeacherSchema().dump(all_teachers, many=True)
    return APIResponse.respond(data=all_teachers_dump)

@principal_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade or re-grade an assignment"""
    grade_payload = AssignmentGradeSchema().load(incoming_payload)
    assignment = Assignment.query.get(grade_payload.id)
    if assignment:
        assignment.grade = grade_payload.grade
        assignment.state = 'GRADED'
        db.session.commit()
        assignment_dump = AssignmentSchema().dump(assignment)
        return APIResponse.respond(data=assignment_dump)
    else:
        return APIResponse.respond_with_error('Assignment not found', status_code=404)

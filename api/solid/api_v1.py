# encoding=utf-8
import json
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from common.helpers import (
    ok_json,
    error_json
)
from solid.models import (
    User,
    CodingLanguage,
    ProjectType,
    Network,
    AuditProject,
    ProjectPeopleComments,
    LoadBoard,
    AskAudit
)

def get_languages(request):
    code_lg_list = CodingLanguage.objects.all().order_by("-id")
    sr_response = []
    for sr in code_lg_list:
        sr_response.append(sr.as_dict())
    return ok_json(sr_response)


# @check_api_token
def get_project_type(request):
    sr_list = ProjectType.objects.all().order_by("-id")
    sr_response = []
    for sr in sr_list:
        sr_response.append(sr.as_dict())
    return ok_json(sr_response)


def get_network_list(request):
    nt_list = Network.objects.all().order_by("-id")
    sr_response = []
    for sr in nt_list:
        sr_response.append(sr.as_dict())
    return ok_json(sr_response)


# @check_api_token
def get_audit_projects(request):
    try:
        params = json.loads(request.body.decode())
    except (ValueError, AttributeError):
        return error_json("invalid params")

    language_id = params.get("language_id")
    project_type_id = params.get("project_type_id")
    network_id = params.get("network_id")
    status = params.get("status", "all").lower()

    filters = Q()
    if project_type_id and str(project_type_id) not in ["0", ""]:
        filters &= Q(project_type__id=project_type_id)
    if language_id and str(language_id) not in ["0", ""]:
        filters &= Q(coding_language__id=language_id)
    if network_id and str(network_id) not in ["0", ""]:
        filters &= Q(network__id=network_id)
    if status not in ["all"]:
        filters &= Q(status=status.capitalize())

    audit_project_lists = (
        AuditProject.objects
        .filter(filters)
        .select_related("project_type", "coding_language", "network")
        .order_by("-id")
    )
    projects_ret_lists = [ap.as_dict() for ap in audit_project_lists]
    data = {
        "total": len(projects_ret_lists),
        "projects": projects_ret_lists
    }
    return ok_json(data)


# @check_api_token
def get_members_comment(request):
    cm_lists = ProjectPeopleComments.objects.all().order_by("-id").all()
    cm_ret_lists = []
    for cm in cm_lists:
        cm_ret_lists.append(cm.as_dict())
    return ok_json(cm_ret_lists)


# @check_api_token
def get_leadboard_list(request):
    leadboard_lists = LoadBoard.objects.all().order_by("-payouts")
    ret_leadboard_lists = []
    for ld in leadboard_lists:
        ret_leadboard_lists.append(ld.as_dict())
    return ok_json(ret_leadboard_lists)

@csrf_exempt
def create_audit_project(request):
    if request.method != "POST":
        return error_json("invalid request method")

    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return error_json("invalid JSON payload")

    name = data.get("name", "")
    project_type_id = data.get("project_type_id")
    coding_language_id = data.get("coding_language_id")
    network_id = data.get("network_id")
    user_id = data.get("user_id")
    start_time = data.get("start_time", "")
    end_time = data.get("end_time", "")
    cycle = data.get("cycle", "")
    status = data.get("status", "Ongoing")
    detail = data.get("detail", "")
    bounty_fund = data.get("bounty_fund", "")
    project_link = data.get("project_link", "")
    report_link = data.get("report_link", "")
    x_link = data.get("x_link", "")
    telegram = data.get("telegram", "")
    discord = data.get("discord", "")
    github = data.get("github", "")
    community_link = data.get("community_link", "")
    bounty_description = data.get("bounty_description", "")

    if not name:
        return error_json("project name is required")

    project = AuditProject.objects.filter(github=github, x_link=x_link).first()
    if project is not None:
        return error_json("project existed now")

    project_type = ProjectType.objects.filter(id=project_type_id).first()
    if project_type is None:
        return error_json("invalid project type")

    coding_language = CodingLanguage.objects.filter(id=coding_language_id).first()
    if coding_language is None:
        return error_json("invalid coding language")

    network = Network.objects.filter(id=network_id).first()
    if network is None:
        return error_json("invalid network")

    user = User.objects.filter(id=user_id).first()
    if user is None:
        return error_json("invalid user")

    try:
        audit_project = AuditProject.objects.create(
            name=name,
            project_type=project_type,
            coding_language=coding_language,
            network=network,
            user=user,
            start_time=start_time,
            end_time=end_time,
            cycle=cycle,
            status=status,
            detail=detail,
            bounty_fund=bounty_fund,
            project_link=project_link,
            report_link=report_link,
            x_link=x_link,
            telegram=telegram,
            discord=discord,
            github=github,
            community_link=community_link,
            bounty_description=bounty_description,
        )
    except Exception as e:
        return error_json("failed to create project")

    return ok_json(audit_project.as_dict())

@csrf_exempt
def submit_ask_audit(request):
    if request.method != "POST":
        return error_json("invalid request method")

    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return error_json("invalid JSON payload")

    repo_link = data.get("repo_link", "").strip()

    if AskAudit.objects.filter(repo_link=repo_link).exists():
        return error_json("project have already submitted")

    ask_audit = AskAudit.objects.create(
        name=data.get("name", ""),
        contact=data.get("contact", ""),
        company=data.get("company", ""),
        completed_time=data.get("completed_time", ""),
        repo_link=repo_link,
        detail=data.get("detail", ""),
        ecosystem=data.get("ecosystem", ""),
        find_us_way=data.get("find_us_way", ""),
        images=data.get("images", ""),
    )

    return ok_json({
        "id": ask_audit.id,
        "name": ask_audit.name,
        "repo_link": ask_audit.repo_link
    })
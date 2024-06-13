# encoding=utf-8

import json
import uuid

from common.helpers import (
    ok_json,
    error_json
)
from solid.models import (
   ServiceType,
   AuditProject,
   CoreMember,
   LoadBoard
)


# @check_api_token
def get_services_type(request):
    sr_list = ServiceType.objects.all().order_by("-id")
    sr_response = []
    for sr in sr_list:
        sr_response.append(sr.as_dict())
    return ok_json(sr_response)


# @check_api_token
def get_audit_projects(request):
    params = json.loads(request.body.decode())
    service_type_id = params.get("service_type_id", 0)
    status = params.get("status", "all")
    service_type = ServiceType.objects.filter(id=service_type_id).first()
    if service_type_id not in ["0", 0] and status in ["all", "All", "ALL"]:
        audit_project_lists = AuditProject.objects.filter(service_type__id=service_type_id).order_by("id").all()
    elif status in ["all", "All", "ALL"]:
        audit_project_lists = AuditProject.objects.all().order_by("id").all()
    else:
        audit_project_lists = AuditProject.objects.filter(status='Ongoing').order_by("id").all()
    projects_ret_lists = []
    for ap in audit_project_lists:
        projects_ret_lists.append(ap.as_dict())
    data = {
        "service_type": service_type.as_dict(),
        "projects": projects_ret_lists
    }
    return ok_json(data)


# @check_api_token
def get_core_members(request):
    cm_lists = CoreMember.objects.all().order_by("-id").all()
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

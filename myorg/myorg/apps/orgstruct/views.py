from django.http import Http404, HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from .models import Worker, Title, Department, Hierarchy
import datetime
from .config import TIME_CASH_HIERARCHY_S


def index(request):
    workers = Worker.objects.order_by("name")
    return render(request, "orgstruct/hierarchy.html", {"workers": workers})


def hierarchy_company(request):
    hierarchy_cashed = Hierarchy.objects.first()
    time_now = datetime.datetime.now(datetime.timezone.utc)

    if hierarchy_cashed is None or time_now - hierarchy_cashed.ttl > datetime.timedelta(seconds=TIME_CASH_HIERARCHY_S):
        hierarchy = Hierarchy.objects.raw(
            """
        WITH RECURSIVE descendants AS (
        SELECT id, parent_id, 0 AS depth
        FROM orgstruct_department
        WHERE parent_id is null
        UNION
            SELECT p.id, p.parent_id, d.depth+ 1
            FROM orgstruct_department p
            INNER JOIN descendants d
            ON p.parent_id = d.id
        ), levels as (
        SELECT p.id, p.name, depth
        FROM descendants d
        INNER JOIN orgstruct_department p
        ON d.id = p.id
        WHERE p.id <> 1)
        select 1 as id, jsonb_agg(r1.res) as data from (
        select jsonb_build_object('level', r.depth, 'departments', jsonb_agg(jsonb_build_object('departments_name', r.name, 'workers', workers))) as res from (
        select od.id, od.name, array_agg(ow."name") as workers, depth from levels od
        left join orgstruct_worker ow ON ow.department_id = od.id 
        group by od.id, od.name, depth
        order by depth) as r
        group by r.depth
        ) as r1
        group by id;
            """
        )[0]

        if hierarchy_cashed is None:
            Hierarchy.objects.create(data=hierarchy.data, ttl=time_now)
        else:
            hierarchy_cashed.data = hierarchy.data
            hierarchy_cashed.ttl = time_now
            hierarchy_cashed.save()
    else:
        hierarchy = Hierarchy.objects.first()
    return render(request, "orgstruct/hierarchy.html", {"hierarchy": hierarchy})


def detail_worker(request, worker_id):
    try:
        worker = Worker.objects.get(id=worker_id)
    except:
        raise Http404("Рабочий не найден")

    return render(request, "orgstruct/worker_info.html", {"worker": worker})

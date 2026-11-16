# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import CommentForm, ServiceRequestForm
from .models import ServiceRequest
from .selectors import service_request_filter, service_request_get
from .services import (
    comment_create,
    service_request_create,
    service_request_update,
)


@login_required
def request_list(request):
    status = request.GET.get("status", "").strip()
    query = request.GET.get("q", "").strip()
    queryset = service_request_filter(
        user=request.user, status=status, query=query
    )
    page_obj = Paginator(queryset, 10).get_page(request.GET.get("page"))
    return render(
        request,
        "requests_app/request_list.html",
        {
            "page_obj": page_obj,
            "status_choices": ServiceRequest.Status.choices,
            "selected_status": status,
            "query": query,
        },
    )


@login_required
def request_detail(request, request_id):
    try:
        item = service_request_get(user=request.user, request_id=request_id)
    except ServiceRequest.DoesNotExist as exc:
        raise Http404("Service request not found.") from exc

    return render(
        request,
        "requests_app/request_detail.html",
        {
            "item": item,
            "comments": item.comments.select_related("author").order_by(
                "created_at"
            ),
            "comment_form": CommentForm(),
        },
    )


@login_required
def request_create(request):
    form = ServiceRequestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        item = service_request_create(
            requester=request.user, **form.cleaned_data
        )
        messages.success(request, "Service request created.")
        return redirect("requests:detail", request_id=item.id)
    return render(
        request,
        "requests_app/request_form.html",
        {"form": form, "mode": "Create"},
    )


@login_required
def request_update(request, request_id):
    try:
        item = service_request_get(user=request.user, request_id=request_id)
    except ServiceRequest.DoesNotExist as exc:
        raise Http404("Service request not found.") from exc

    form = ServiceRequestForm(request.POST or None, instance=item)
    if request.method == "POST" and form.is_valid():
        try:
            item = service_request_update(
                item=item, actor=request.user, **form.cleaned_data
            )
        except ValidationError as exc:
            form.add_error(None, exc)
        else:
            messages.success(request, "Service request updated.")
            return redirect("requests:detail", request_id=item.id)

    return render(
        request,
        "requests_app/request_form.html",
        {"form": form, "mode": "Update", "item": item},
    )


@require_POST
@login_required
def comment_add(request, request_id):
    try:
        item = service_request_get(user=request.user, request_id=request_id)
    except ServiceRequest.DoesNotExist as exc:
        raise Http404("Service request not found.") from exc

    form = CommentForm(request.POST)
    if form.is_valid():
        comment_create(item=item, author=request.user, **form.cleaned_data)
        messages.success(request, "Comment added.")
    else:
        messages.error(request, "Enter at least 3 characters.")
    return redirect("requests:detail", request_id=item.id)

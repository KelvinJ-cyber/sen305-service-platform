from django.contrib import admin
from django.utils import timezone

# Register your models here.

from django.contrib import admin

from .models import Category, Comment, ServiceRequest, WorkOrder


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "description")


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ("author", "body", "is_internal", "created_at")
    readonly_fields = ("created_at",)

class OverdueFilter(admin.SimpleListFilter):
    title = "overdue status"
    parameter_name = "overdue"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Overdue"),
            ("no", "Not overdue"),
        )

    def queryset(self, request, queryset):
        now = timezone.now()

        active_statuses = [
            "open",
            "assigned",
            "in_progress",
        ]

        if self.value() == "yes":
            return queryset.filter(
                due_at__lt=now,
                status__in=active_statuses,
            )

        if self.value() == "no":
            return queryset.exclude(
                due_at__lt=now,
                status__in=active_statuses,
            )

        return queryset

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "requester",
        "priority",
        "status",
        "due_at",
        "resolution_summary",
        "created_at",
    )

    list_filter = ("status", "priority", "category", OverdueFilter)

    search_fields = (
        "title",
        "description",
        "location",
        "requester__username",
        "resolution_summary",
    )

    readonly_fields = ("id", "created_at", "updated_at")

    autocomplete_fields = ("requester", "category")

    date_hierarchy = "created_at"

    inlines = (CommentInline,)


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = (
        "service_request",
        "technician",
        "started_at",
        "completed_at",
    )

    search_fields = (
        "service_request__title",
        "technician__username",
    )

    autocomplete_fields = ("service_request", "technician")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "service_request",
        "author",
        "is_internal",
        "created_at",
    )

    list_filter = ("is_internal", "created_at")

    search_fields = (
        "body",
        "service_request__title",
        "author__username",
    )


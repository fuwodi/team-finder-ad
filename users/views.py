import json
from http import HTTPStatus

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from users.forms import (
    LoginForm,
    ProfileEditForm,
    RegistrationForm,
    UserPasswordChangeForm,
)
from users.models import Skill, User

PAGE_SIZE = 12
SKILLS_AUTOCOMPLETE_LIMIT = 10


def register_view(request):
    if request.user.is_authenticated:
        return redirect("projects:list")

    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("projects:list")

    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("projects:list")

    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("projects:list")

    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("projects:list")


def user_list_view(request):
    participants = User.objects.all().order_by("-id")
    active_skill = request.GET.get("skill", "").strip()

    if active_skill:
        participants = participants.filter(skills__name=active_skill).distinct()

    paginator = Paginator(participants, PAGE_SIZE)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "users/participants.html",
        {
            "participants": page_obj,
            "page_obj": page_obj,
            "all_skills": Skill.objects.all().order_by("name"),
            "active_skill": active_skill,
        },
    )


def user_detail_view(request, pk):
    profile_user = get_object_or_404(
        User.objects.prefetch_related("owned_projects", "skills"),
        pk=pk,
    )
    return render(
        request,
        "users/user-details.html",
        {"user": profile_user},
    )


@login_required
def edit_profile_view(request):
    form = ProfileEditForm(
        request.POST or None,
        request.FILES or None,
        instance=request.user,
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("users:detail", pk=request.user.pk)

    return render(
        request,
        "users/edit_profile.html",
        {"form": form, "user": request.user},
    )


@login_required
def change_password_view(request):
    form = UserPasswordChangeForm(request.user, request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        login(request, request.user)
        return redirect("users:detail", pk=request.user.pk)

    return render(request, "users/change_password.html", {"form": form})


@require_GET
def skills_autocomplete_view(request):
    query = request.GET.get("q", "").strip()
    skills = Skill.objects.filter(name__istartswith=query).order_by("name")[
        :SKILLS_AUTOCOMPLETE_LIMIT
    ]
    data = [{"id": skill.id, "name": skill.name} for skill in skills]
    return JsonResponse(data, safe=False)


@login_required
@require_POST
def skill_add_view(request, pk):
    profile_user = User.objects.filter(pk=pk).first()
    if profile_user is None:
        return JsonResponse(
            {"error": "user not found"},
            status=HTTPStatus.NOT_FOUND,
        )
    if profile_user != request.user:
        return JsonResponse({"error": "forbidden"}, status=HTTPStatus.FORBIDDEN)

    try:
        payload = json.loads(request.body.decode())
    except json.JSONDecodeError:
        payload = request.POST

    skill = None
    created = False
    skill_id = payload.get("skill_id")
    name = (payload.get("name") or "").strip()

    if skill_id:
        skill = Skill.objects.filter(pk=skill_id).first()
        if skill is None:
            return JsonResponse(
                {"error": "skill not found"},
                status=HTTPStatus.NOT_FOUND,
            )
    elif name:
        skill, created = Skill.objects.get_or_create(name=name)
    else:
        return JsonResponse(
            {"error": "invalid data"},
            status=HTTPStatus.BAD_REQUEST,
        )

    added = not profile_user.skills.filter(pk=skill.pk).exists()
    if added:
        profile_user.skills.add(skill)

    return JsonResponse(
        {
            "skill_id": skill.id,
            "name": skill.name,
            "created": created,
            "added": added,
        }
    )


@login_required
@require_POST
def skill_remove_view(request, pk, skill_id):
    profile_user = User.objects.filter(pk=pk).first()
    if profile_user is None:
        return JsonResponse(
            {"error": "user not found"},
            status=HTTPStatus.NOT_FOUND,
        )
    if profile_user != request.user:
        return JsonResponse({"error": "forbidden"}, status=HTTPStatus.FORBIDDEN)

    skill = Skill.objects.filter(pk=skill_id).first()
    if skill is None:
        return JsonResponse(
            {"error": "skill not found"},
            status=HTTPStatus.NOT_FOUND,
        )
    if profile_user.skills.filter(pk=skill.pk).exists():
        profile_user.skills.remove(skill)
        return JsonResponse({"status": "ok"})

    return JsonResponse(
        {"error": "skill not found"},
        status=HTTPStatus.NOT_FOUND,
    )

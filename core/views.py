import mimetypes
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Prefetch
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render

from blog.models import Post

from .forms import ContactForm
from .models import (
    Achievement,
    CodingProfile,
    Education,
    Experience,
    Language,
    Profile,
    Project,
    Skill,
    SkillCategory,
)


def _base_context():
    return {
        "profile": Profile.objects.filter(is_active=True).first(),
        "skill_categories": SkillCategory.objects.prefetch_related(
            Prefetch("skills", queryset=Skill.objects.order_by("order", "name"))
        ),
        "education": Education.objects.all(),
        "experiences": Experience.objects.prefetch_related("bullets"),
        "awards": Achievement.objects.filter(kind="award"),
        "certifications": Achievement.objects.filter(kind="cert"),
        "coding_profiles": CodingProfile.objects.all(),
        "languages": Language.objects.all(),
    }


def home(request):
    context = _base_context()
    context.update(
        {
            "projects": Project.objects.all()[:6],
            "featured_projects": Project.objects.filter(is_featured=True)[:3],
            "recent_posts": Post.published.select_related("category")[:3],
            "form": ContactForm(),
            "project_count": Project.objects.count(),
        }
    )
    return render(request, "core/home.html", context)


def project_list(request):
    projects = Project.objects.all()
    active_category = request.GET.get("category", "")
    if active_category:
        projects = projects.filter(category=active_category)

    query = request.GET.get("q", "").strip()
    if query:
        projects = projects.filter(title__icontains=query) | projects.filter(
            tech_stack__icontains=query
        )

    return render(
        request,
        "core/project_list.html",
        {
            "projects": projects.distinct(),
            "categories": Project.CATEGORY_CHOICES,
            "active_category": active_category,
            "query": query,
        },
    )


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    related = Project.objects.filter(category=project.category).exclude(pk=project.pk)[:3]
    return render(request, "core/project_detail.html", {"project": project, "related": related})


def resume_download(request):
    """Serve the resume from the Profile record, falling back to a static copy."""
    profile = Profile.objects.filter(is_active=True).first()
    if profile and profile.resume:
        return FileResponse(
            profile.resume.open("rb"),
            as_attachment=True,
            filename=Path(profile.resume.name).name,
        )

    fallback = Path(settings.BASE_DIR) / "static" / "files" / "resume.pdf"
    if fallback.exists():
        content_type = mimetypes.guess_type(str(fallback))[0] or "application/pdf"
        return FileResponse(
            open(fallback, "rb"),
            as_attachment=True,
            filename="Chandra_Mouli_Kilari_Resume.pdf",
            content_type=content_type,
        )
    raise Http404("Resume has not been uploaded yet.")


def contact(request):
    if request.method != "POST":
        return redirect("core:home")

    form = ContactForm(request.POST)
    if form.is_valid():
        contact_message = form.save()
        try:
            send_mail(
                subject=f"[Portfolio] {contact_message.subject or 'New message'} "
                f"from {contact_message.name}",
                message=f"From: {contact_message.name} <{contact_message.email}>\n\n"
                f"{contact_message.message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_NOTIFY_EMAIL],
                fail_silently=True,
            )
        except Exception:  # pragma: no cover - never break the UX over email
            pass
        messages.success(request, "Thanks for reaching out — I'll get back to you soon.")
        return redirect("/#contact")

    context = _base_context()
    context.update(
        {
            "projects": Project.objects.all()[:6],
            "recent_posts": Post.published.select_related("category")[:3],
            "form": form,
            "project_count": Project.objects.count(),
        }
    )
    messages.error(request, "Please fix the errors below and resend.")
    return render(request, "core/home.html", context)


def custom_404(request, exception):  # pragma: no cover
    return render(request, "404.html", status=404)


def custom_500(request):  # pragma: no cover
    return render(request, "500.html", status=500)

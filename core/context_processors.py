from .models import Profile


def site_profile(request):
    """Make the active profile available to every template (nav, footer, meta tags)."""
    return {"site_profile": Profile.objects.filter(is_active=True).first()}

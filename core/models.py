from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    """Abstract base giving every row created/updated timestamps."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Profile(TimeStampedModel):
    """Singleton-ish model holding the site owner's identity and hero copy."""

    full_name = models.CharField(max_length=120)
    tagline = models.CharField(
        max_length=160, help_text="Short role line, e.g. 'Developer ~ Engineer'"
    )
    typed_roles = models.CharField(
        max_length=300,
        blank=True,
        help_text="Comma-separated roles cycled by the typing animation in the hero.",
    )
    about = models.TextField(help_text="Two or three paragraphs. Blank lines separate paragraphs.")
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    location = models.CharField(max_length=120, blank=True)
    github_username = models.CharField(max_length=80, blank=True)
    linkedin_url = models.URLField(blank=True)
    photo = models.ImageField(upload_to="profile/", blank=True, null=True)
    resume = models.FileField(
        upload_to="resume/", blank=True, null=True, help_text="PDF served by the download button."
    )
    available_for_work = models.BooleanField(default=True)
    is_active = models.BooleanField(
        default=True, help_text="The first active profile is the one the site renders."
    )

    class Meta:
        ordering = ["-is_active", "full_name"]

    def __str__(self):
        return self.full_name

    @property
    def roles_list(self):
        return [role.strip() for role in self.typed_roles.split(",") if role.strip()]

    @property
    def about_paragraphs(self):
        return [para.strip() for para in self.about.split("\n\n") if para.strip()]

    @property
    def github_url(self):
        return f"https://github.com/{self.github_username}" if self.github_username else ""


class SkillCategory(TimeStampedModel):
    """A named grouping such as 'Machine Learning' or 'Web Development'."""

    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(
        max_length=60,
        blank=True,
        default="bi-code-slash",
        help_text="Bootstrap Icons class, e.g. 'bi-cpu'.",
    )
    description = models.CharField(max_length=250, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "Skill categories"

    def __str__(self):
        return self.name


class Skill(TimeStampedModel):
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=100)
    proficiency = models.PositiveSmallIntegerField(
        default=80, help_text="0-100, drives the progress bar width."
    )
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        unique_together = ("category", "name")

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Education(TimeStampedModel):
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=150)
    field_of_study = models.CharField(max_length=150, blank=True)
    location = models.CharField(max_length=120, blank=True)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(null=True, blank=True, help_text="Blank = present.")
    score = models.CharField(max_length=60, blank=True, help_text="e.g. 'Aggregate: 89.7%'")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-start_year"]
        verbose_name_plural = "Education"

    def __str__(self):
        return f"{self.degree} — {self.institution}"

    @property
    def period(self):
        return f"{self.start_year} – {self.end_year or 'Present'}"


class Experience(TimeStampedModel):
    role = models.CharField(max_length=150)
    organisation = models.CharField(max_length=200)
    location = models.CharField(max_length=120, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True, help_text="Blank = current role.")
    summary = models.TextField(blank=True)
    tech_stack = models.CharField(
        max_length=300, blank=True, help_text="Comma-separated technologies."
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-start_date"]

    def __str__(self):
        return f"{self.role} @ {self.organisation}"

    @property
    def tech_list(self):
        return [t.strip() for t in self.tech_stack.split(",") if t.strip()]

    @property
    def period(self):
        start = self.start_date.strftime("%b %Y")
        end = self.end_date.strftime("%b %Y") if self.end_date else "Present"
        return f"{start} – {end}"


class ExperienceBullet(models.Model):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name="bullets")
    text = models.CharField(max_length=400)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.text[:60]


class Project(TimeStampedModel):
    CATEGORY_CHOICES = [
        ("ml", "Machine Learning"),
        ("dl", "Deep Learning"),
        ("nlp", "NLP / LLM"),
        ("web", "Full Stack Web"),
        ("ds", "Data Science"),
        ("other", "Other"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    subtitle = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default="ml")
    short_description = models.TextField(help_text="One or two sentences shown on the card.")
    description = models.TextField(blank=True, help_text="Full write-up on the detail page.")
    highlights = models.TextField(
        blank=True, help_text="One achievement per line — rendered as a bullet list."
    )
    tech_stack = models.CharField(max_length=300, help_text="Comma-separated technologies.")
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    badge = models.CharField(
        max_length=60, blank=True, help_text="Small ribbon text, e.g. 'M.Tech Thesis'."
    )
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:220]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:project_detail", kwargs={"slug": self.slug})

    @property
    def tech_list(self):
        return [t.strip() for t in self.tech_stack.split(",") if t.strip()]

    @property
    def highlight_list(self):
        return [h.strip("•- ").strip() for h in self.highlights.splitlines() if h.strip()]


class Achievement(TimeStampedModel):
    """Awards, positions of responsibility and certifications share one shape."""

    KIND_CHOICES = [
        ("award", "Award / Achievement"),
        ("cert", "Certification"),
    ]

    kind = models.CharField(max_length=10, choices=KIND_CHOICES, default="award")
    title = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200, blank=True)
    period = models.CharField(max_length=60, blank=True, help_text="e.g. '2023 – 2024'")
    description = models.TextField(blank=True, help_text="One point per line.")
    url = models.URLField(blank=True)
    icon = models.CharField(max_length=60, blank=True, default="bi-trophy")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title

    @property
    def point_list(self):
        return [p.strip("•- ").strip() for p in self.description.splitlines() if p.strip()]


class CodingProfile(TimeStampedModel):
    platform = models.CharField(max_length=80)
    username = models.CharField(max_length=100)
    url = models.URLField()
    icon = models.CharField(max_length=60, blank=True, default="bi-code-square")
    stat_label = models.CharField(
        max_length=60, blank=True, help_text="Optional, e.g. 'Problems solved'."
    )
    stat_value = models.CharField(max_length=60, blank=True, help_text="Optional, e.g. '350+'.")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "platform"]

    def __str__(self):
        return f"{self.platform} — {self.username}"


class Language(TimeStampedModel):
    name = models.CharField(max_length=60)
    level = models.CharField(max_length=60, default="Fluent")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return f"{self.name} ({self.level})"


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} <{self.email}> — {self.subject or 'No subject'}"

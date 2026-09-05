"""
Seed the portfolio with Chandra Mouli Kilari's CV content.

    python manage.py seed_portfolio          # add/update rows
    python manage.py seed_portfolio --flush  # wipe portfolio tables first
"""
from datetime import date

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from blog.models import Category, Post
from core.models import (
    Achievement,
    CodingProfile,
    Education,
    Experience,
    ExperienceBullet,
    Language,
    Profile,
    Project,
    Skill,
    SkillCategory,
)


class Command(BaseCommand):
    help = "Populate the database with portfolio content from the CV."

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete existing portfolio rows before seeding.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["flush"]:
            for model in (
                ExperienceBullet, Experience, Skill, SkillCategory, Education,
                Project, Achievement, CodingProfile, Language, Profile, Post, Category,
            ):
                model.objects.all().delete()
            self.stdout.write(self.style.WARNING("Existing portfolio data removed."))

        self._profile()
        self._skills()
        self._education()
        self._experience()
        self._projects()
        self._achievements()
        self._coding_profiles()
        self._languages()
        self._blog()

        self.stdout.write(self.style.SUCCESS("Portfolio seeded successfully."))

    # ------------------------------------------------------------------ profile
    def _profile(self):
        Profile.objects.update_or_create(
            full_name="Chandra Mouli Kilari",
            defaults={
                "tagline": "Developer ~ Engineer",
                "typed_roles": "machine learning systems, deep learning models, "
                "NLP & LLM pipelines, full-stack web apps",
                "about": (
                    "I'm an M.Tech student in Information Technology at ABV-IIITM Gwalior, "
                    "working at the intersection of machine learning research and software "
                    "engineering. My thesis benchmarks 21 forecasting models for photovoltaic "
                    "power across 4,928 evaluations — work that taught me as much about "
                    "auditing broken pipelines as about building new ones.\n\n"
                    "I like problems where the modelling and the engineering both matter: "
                    "training a 10.7M-parameter Transformer from scratch, then wrapping the "
                    "retrieval pipeline in something people can actually use. I write Python "
                    "and C++ daily, build web apps with Django and Flask, and care a lot about "
                    "reproducible, leakage-free evaluation.\n\n"
                    "Outside coursework I've interned as a Data Science Intern at APSSDC, "
                    "reached the finals of the Hitachi 30 Hacks hackathon with a blockchain "
                    "payments app, and served as Joint Secretary of my college coding club."
                ),
                "email": "chandramoulikilari3@gmail.com",
                "phone": "+91 8008163537",
                "location": "Gwalior, Madhya Pradesh, India",
                "github_username": "kilarichandramouli",
                "linkedin_url": "https://www.linkedin.com/in/kilarichandramouli",
                "available_for_work": True,
                "is_active": True,
            },
        )
        self.stdout.write("  · profile")

    # ------------------------------------------------------------------- skills
    def _skills(self):
        data = [
            ("Programming Languages", "bi-code-slash", "Languages I'm fluent in day to day.", 1, [
                ("Python", 95, True), ("C++", 85, True), ("C", 80, True), ("SQL", 80, False),
            ]),
            ("Machine Learning", "bi-cpu", "Classical ML end to end.", 2, [
                ("Supervised Learning", 90, True), ("Unsupervised Learning", 85, True),
                ("Feature Engineering", 0, False), ("Model Evaluation", 0, False),
                ("Scikit-learn", 0, False), ("XGBoost", 0, False), ("LightGBM", 0, False),
            ]),
            ("Deep Learning", "bi-diagram-3", "Neural architectures and optimisation.", 3, [
                ("Neural Networks (ANN, CNN, RNN)", 88, True), ("LSTM / GRU", 0, False),
                ("Model Optimization", 0, False), ("TensorFlow", 0, False), ("PyTorch", 0, False),
            ]),
            ("LLMs & NLP", "bi-chat-square-text", "Language models, retrieval and text pipelines.", 4, [
                ("Transformers", 90, True), ("RAG", 88, True), ("Prompt Engineering", 0, False),
                ("Hugging Face", 0, False), ("Tokenization", 0, False), ("Embeddings", 0, False),
                ("N-gram Models", 0, False), ("HMM", 0, False),
            ]),
            ("Data Science & Analysis", "bi-bar-chart-line", "Getting signal out of messy data.", 5, [
                ("Exploratory Data Analysis", 88, True), ("Data Cleaning", 0, False),
                ("Data Visualization", 0, False), ("Pandas", 0, False), ("NumPy", 0, False),
            ]),
            ("Time Series & Forecasting", "bi-graph-up-arrow", "M.Tech thesis territory.", 6, [
                ("Single & Multi-Step Forecasting", 90, True), ("Lag Features", 0, False),
                ("Statistical Analysis", 0, False), ("Leakage-safe Evaluation", 0, False),
            ]),
            ("Web Development", "bi-window-stack", "Full-stack, mostly Python-backed.", 7, [
                ("Django", 88, True), ("HTML / CSS", 90, True), ("JavaScript", 82, True),
                ("Bootstrap", 0, False), ("Flask", 0, False), ("Streamlit", 0, False),
            ]),
            ("Core CS & Tools", "bi-hdd-stack", "The fundamentals interviewers ask about.", 8, [
                ("Data Structures & Algorithms", 90, True), ("OOP", 0, False), ("DBMS", 0, False),
                ("Operating Systems", 0, False), ("Computer Networks", 0, False),
                ("Git / GitHub", 0, False),
            ]),
        ]

        for name, icon, description, order, skills in data:
            category, _ = SkillCategory.objects.update_or_create(
                name=name,
                defaults={"icon": icon, "description": description, "order": order},
            )
            for index, (skill_name, proficiency, featured) in enumerate(skills):
                Skill.objects.update_or_create(
                    category=category,
                    name=skill_name,
                    defaults={
                        "proficiency": proficiency or 80,
                        "is_featured": featured,
                        "order": index,
                    },
                )
        self.stdout.write("  · skills")

    # ---------------------------------------------------------------- education
    def _education(self):
        entries = [
            ("Atal Bihari Vajpayee Indian Institute of Information Technology and Management",
             "M.Tech", "Information Technology", "Gwalior, MP", 2025, None, "Aggregate: 100%", 1),
            ("Rajiv Gandhi University of Knowledge Technologies",
             "B.Tech", "Computer Science and Engineering", "Srikakulam, AP", 2021, 2025,
             "Aggregate: 89.7%", 2),
            ("Rajiv Gandhi University of Knowledge Technologies",
             "Intermediate", "Maths, Physics and Chemistry", "Srikakulam, AP", 2019, 2021,
             "Aggregate: 98.3%", 3),
            ("A.P Model School, Ganguvari Sigadam",
             "SSC", "", "Andhra Pradesh", 2018, 2019, "Aggregate: 100%", 4),
        ]
        for inst, degree, field, loc, start, end, score, order in entries:
            Education.objects.update_or_create(
                institution=inst,
                degree=degree,
                defaults={
                    "field_of_study": field,
                    "location": loc,
                    "start_year": start,
                    "end_year": end,
                    "score": score,
                    "order": order,
                },
            )
        self.stdout.write("  · education")

    # --------------------------------------------------------------- experience
    def _experience(self):
        experience, _ = Experience.objects.update_or_create(
            role="Data Science Intern",
            organisation="Andhra Pradesh State Skill Development Corporation (APSSDC)",
            defaults={
                "location": "Andhra Pradesh, India",
                "start_date": date(2024, 5, 1),
                "end_date": date(2024, 6, 30),
                "summary": "Built and shipped an end-to-end sentiment analysis pipeline over "
                           "real customer feedback data.",
                "tech_stack": "Python, Machine Learning, NLP, Scikit-learn, Pandas, NLTK",
                "order": 1,
            },
        )
        bullets = [
            "Developed an NLP-based sentiment analysis model achieving 88% accuracy.",
            "Processed and analyzed 5,000+ records using data cleaning, preprocessing and feature engineering.",
            "Improved data quality by 30% through effective preprocessing and validation techniques.",
            "Optimized the inference pipeline, reducing prediction time by 20%.",
        ]
        experience.bullets.all().delete()
        for index, text in enumerate(bullets):
            ExperienceBullet.objects.create(experience=experience, text=text, order=index)
        self.stdout.write("  · experience")

    # ----------------------------------------------------------------- projects
    def _projects(self):
        projects = [
            {
                "title": "Large-Scale Benchmarking Pipeline for Photovoltaic Power Forecasting",
                "subtitle": "21 models · 4 sites · 7 horizons · 4,928 evaluations",
                "category": "dl",
                "badge": "M.Tech Thesis",
                "short_description": "A reproducible benchmark of 21 forecasting models for solar "
                                     "power across 4 sites, 7 horizons and 2 temporal resolutions — "
                                     "plus an audit that overturned the study's original conclusion.",
                "description": (
                    "Implemented Informer, Autoformer, FEDformer and the Temporal Fusion Transformer "
                    "directly from their source papers, alongside statistical and gradient-boosted "
                    "baselines, and evaluated every combination of site, horizon and resolution.\n"
                    "Audited the existing forecasting pipeline and fixed 13 defects. The critical one "
                    "returned single-step forecasts under multi-step labels, which made statistical "
                    "models look better than deep learning at long horizons; correcting it reversed "
                    "the finding entirely.\n"
                    "Rebuilt evaluation on leakage-safe foundations: chronological splits, train/test "
                    "embargoes, and scaling fitted only on the training block."
                ),
                "highlights": "4,928 model evaluations across 21 architectures\n"
                              "Reimplemented 4 transformer forecasters from their papers\n"
                              "Found and fixed 13 pipeline defects, one of which inverted the conclusion\n"
                              "Leakage-safe chronological splits with train/test embargoes",
                "tech_stack": "Python, PyTorch, TensorFlow, Transformers, XGBoost, pandas, NumPy",
                "is_featured": True,
                "order": 1,
            },
            {
                "title": "Retrieval-Augmented Narrative Consistency Verification",
                "subtitle": "A 10.7M-parameter Transformer trained from scratch",
                "category": "nlp",
                "badge": "Research",
                "short_description": "Designed and trained a BERT-style Transformer with a hybrid "
                                     "BM25 + semantic retrieval RAG pipeline to verify whether "
                                     "narrative statements stay consistent with their source text.",
                "description": (
                    "Rather than fine-tuning an off-the-shelf checkpoint, the encoder was designed and "
                    "trained from scratch at 10.7M parameters so every architectural choice could be "
                    "ablated.\n"
                    "Retrieval combines lexical BM25 with dense semantic search, so the model sees "
                    "evidence that keyword search alone would miss and vice versa."
                ),
                "highlights": "97.56% accuracy on the verification task\n"
                              "0.97 Macro F1 and 0.99 ROC-AUC\n"
                              "Hybrid BM25 + dense retrieval for evidence selection\n"
                              "10.7M-parameter encoder trained from scratch",
                "tech_stack": "PyTorch, Transformers, RAG, BM25, NLP, Python",
                "is_featured": True,
                "order": 2,
            },
            {
                "title": "AI-Powered Multimodal E-commerce Price Prediction System",
                "subtitle": "Text + image features feeding a stacked ensemble",
                "category": "ml",
                "badge": "End-to-end",
                "short_description": "An end-to-end system predicting e-commerce product prices from "
                                     "both product descriptions and product images, served through a "
                                     "Streamlit app for real-time predictions.",
                "description": (
                    "Textual features cover keywords, quality indicators and numeric analysis of the "
                    "listing copy; deep image features come from pre-trained MobileNetV2 and ResNet50 "
                    "backbones.\n"
                    "Predictions come from a super ensemble of XGBoost, LightGBM, Random Forest, "
                    "Gradient Boosting and Ridge Regression, with automated reporting built into the "
                    "Streamlit interface."
                ),
                "highlights": "Multimodal features from product text and images\n"
                              "MobileNetV2 and ResNet50 used as frozen feature extractors\n"
                              "Five-model stacked ensemble for the final prediction\n"
                              "Streamlit app for real-time pricing and automated reports",
                "tech_stack": "Python, TensorFlow, Scikit-learn, XGBoost, LightGBM, Streamlit, NLP",
                "is_featured": True,
                "order": 3,
            },
            {
                "title": "COIN — Currency Operating Interface Navigation",
                "subtitle": "Blockchain-backed group payments with a voice assistant",
                "category": "web",
                "badge": "Hackathon Finalist",
                "short_description": "A digital payments application built on customised blockchain "
                                     "technology, supporting group transactions and an integrated "
                                     "voice assistant. Finalist at the Hitachi 30 Hacks hackathon.",
                "description": (
                    "COIN reimagines everyday payments around groups rather than individuals: splitting, "
                    "settling and tracking shared expenses are first-class operations rather than "
                    "afterthoughts.\n"
                    "A voice assistant layer lets users initiate and confirm transactions hands-free, "
                    "and the customised blockchain layer keeps a verifiable ledger of group activity."
                ),
                "highlights": "Finalist at the Hitachi 30 Hacks Hackathon, Delhi 2024\n"
                              "Group transaction flows built on a customised blockchain\n"
                              "Integrated voice assistant for hands-free payments\n"
                              "Full-stack build across frontend, backend and ledger",
                "tech_stack": "Full Stack Web, Blockchain, JavaScript, Python, HTML, CSS",
                "is_featured": False,
                "order": 4,
            },
        ]

        for data in projects:
            Project.objects.update_or_create(title=data["title"], defaults=data)
        self.stdout.write("  · projects")

    # ------------------------------------------------------------- achievements
    def _achievements(self):
        awards = [
            {
                "title": "Joint Secretary, SGC Coding Club",
                "issuer": "RGUKT Srikakulam",
                "period": "2022 – 2024",
                "icon": "bi-people",
                "description": "Conducted tests on HackerRank to sharpen students' coding skills.\n"
                               "Organised coding events and workshops that grew participation.\n"
                               "Built a competitive programming culture on campus.",
                "order": 1,
            },
            {
                "title": "Finalist — HITACHI 30 Hacks Hackathon",
                "issuer": "Hitachi Group",
                "period": "2023 – 2024",
                "icon": "bi-trophy",
                "description": "Reached the finals with COIN, a blockchain-based digital payments app.\n"
                               "Recognised for group transactions and voice-assistant innovation.",
                "order": 2,
            },
            {
                "title": "Event Organizer, College Tech Fest",
                "issuer": "RGUKT Srikakulam",
                "period": "2023 – 2024",
                "icon": "bi-calendar-event",
                "description": "Managed logistics and scheduling for technical events.\n"
                               "Collaborated with faculty and students on sessions and showcases.",
                "order": 3,
            },
            {
                "title": "Qualified GATE 2025",
                "issuer": "IIT / GATE",
                "period": "2025",
                "icon": "bi-patch-check",
                "description": "Qualified GATE 2025, demonstrating command of core engineering subjects.",
                "order": 4,
            },
        ]
        certifications = [
            {
                "title": "First Place — Code-O-Fiesta, Teckzite 2022",
                "issuer": "RGUKT Nuzvid",
                "period": "2022 – 2023",
                "icon": "bi-award",
                "order": 1,
            },
            {
                "title": "Hackathon Participation — COIN Project",
                "issuer": "Hitachi Group, Delhi",
                "period": "2023 – 2024",
                "icon": "bi-patch-check",
                "order": 2,
            },
        ]

        for data in awards:
            Achievement.objects.update_or_create(
                title=data["title"], kind="award", defaults={**data, "kind": "award"}
            )
        for data in certifications:
            Achievement.objects.update_or_create(
                title=data["title"], kind="cert", defaults={**data, "kind": "cert"}
            )
        self.stdout.write("  · achievements")

    # ----------------------------------------------------------- coding profiles
    def _coding_profiles(self):
        entries = [
            ("LeetCode", "Mouli2025008", "https://leetcode.com/u/Mouli2025008/", "bi-code-square", 1),
            ("GeeksforGeeks", "Mouligfg",
             "https://www.geeksforgeeks.org/user/Mouligfg/", "bi-braces", 2),
            ("HackerRank", "Moulihr", "https://www.hackerrank.com/profile/Moulihr", "bi-terminal", 3),
        ]
        for platform, username, url, icon, order in entries:
            CodingProfile.objects.update_or_create(
                platform=platform,
                defaults={"username": username, "url": url, "icon": icon, "order": order},
            )
        self.stdout.write("  · coding profiles")

    # ---------------------------------------------------------------- languages
    def _languages(self):
        for order, (name, level) in enumerate([("English", "Fluent"), ("Telugu", "Fluent")], 1):
            Language.objects.update_or_create(name=name, defaults={"level": level, "order": order})
        self.stdout.write("  · languages")

    # --------------------------------------------------------------------- blog
    def _blog(self):
        ml_category, _ = Category.objects.get_or_create(name="Machine Learning")
        web_category, _ = Category.objects.get_or_create(name="Web Development")

        posts = [
            {
                "title": "The bug that reversed my thesis conclusion",
                "category": ml_category,
                "tags": "forecasting, debugging, evaluation, transformers",
                "excerpt": "For weeks the statistical baselines beat every deep learning model at "
                           "long horizons. The models were fine. The evaluation was not.",
                "body": (
                    "Every benchmark I ran told the same story: at long forecast horizons, humble "
                    "statistical models outperformed Informer, Autoformer and FEDformer. It was a "
                    "clean, publishable, counterintuitive result — the kind you should distrust.\n\n"
                    "The pipeline was returning single-step forecasts while labelling them as "
                    "multi-step. A one-step-ahead prediction is a far easier problem than a "
                    "24-step-ahead one, so the baselines were being scored on an easy task while the "
                    "deep models were doing the hard one. Correcting the alignment reversed the "
                    "ranking completely.\n\n"
                    "That was one of thirteen defects I found while auditing the pipeline. The lesson "
                    "was not about transformers at all: a result that flatters your baselines deserves "
                    "the same scrutiny as one that flatters your novel method. Now every pipeline I "
                    "build gets chronological splits, train/test embargoes, and scaling fitted on the "
                    "training block only — before I look at a single metric."
                ),
                "status": Post.Status.PUBLISHED,
                "published_at": timezone.now() - timezone.timedelta(days=12),
            },
            {
                "title": "Why I trained a 10.7M-parameter Transformer from scratch",
                "category": ml_category,
                "tags": "transformers, RAG, NLP, PyTorch",
                "excerpt": "Fine-tuning a checkpoint would have been faster. Building the encoder "
                           "myself is what actually taught me how attention behaves.",
                "body": (
                    "The obvious move for narrative consistency verification is to fine-tune a "
                    "pre-trained BERT. I built a 10.7M-parameter encoder from scratch instead, and I'd "
                    "make the same call again.\n\n"
                    "At that scale every architectural decision is observable. Change the head count, "
                    "the layer depth or the positional scheme, and you see the effect in hours, not "
                    "days. Ablations stop being a formality and become the way you actually understand "
                    "the model.\n\n"
                    "The retrieval side mattered just as much. Pairing lexical BM25 with dense "
                    "semantic search surfaced evidence that neither method found alone — exact-name "
                    "matches that embeddings blurred, and paraphrases that keywords missed entirely. "
                    "The final system reached 97.56% accuracy with a 0.99 ROC-AUC, but the retrieval "
                    "quality moved that number more than any modelling change did."
                ),
                "status": Post.Status.PUBLISHED,
                "published_at": timezone.now() - timezone.timedelta(days=30),
            },
            {
                "title": "Building this portfolio with Django instead of static HTML",
                "category": web_category,
                "tags": "django, bootstrap, python, web",
                "excerpt": "Hardcoding a portfolio in HTML is faster on day one and painful on day "
                           "sixty. Here's what the database bought me.",
                "body": (
                    "This site could have been one long index.html. Instead every section — projects, "
                    "skills, education, achievements, blog posts — is a Django model, edited through "
                    "the admin.\n\n"
                    "The practical payoff is that adding a project takes a form submission, not a "
                    "deploy. Filtering, search and pagination come nearly free from the ORM. The "
                    "contact form saves to the database and shows unread messages in the admin, so "
                    "nothing depends on an SMTP server being configured correctly.\n\n"
                    "The interview payoff is bigger. 'I built my own portfolio CMS' invites questions "
                    "about models, migrations, query optimisation and the admin — all things I can "
                    "talk about at length because I made the decisions. A static page invites no "
                    "questions at all."
                ),
                "status": Post.Status.PUBLISHED,
                "published_at": timezone.now() - timezone.timedelta(days=3),
            },
        ]

        for data in posts:
            Post.objects.update_or_create(title=data["title"], defaults=data)
        self.stdout.write("  · blog posts")

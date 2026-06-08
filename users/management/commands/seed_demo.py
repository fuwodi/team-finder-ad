from django.core.management.base import BaseCommand

from projects.models import Project
from users.models import Skill, User


class Command(BaseCommand):
    help = "Создаёт демонстрационных пользователей и проекты для проверки."

    def handle(self, *args, **options):
        if User.objects.filter(email="demo1@example.com").exists():
            self.stdout.write("Демо-данные уже существуют.")
            return

        user1 = User.objects.create_user(
            "demo1@example.com",
            "pass12345",
            name="Иван",
            surname="Иванов",
            phone="89001112233",
        )
        user2 = User.objects.create_user(
            "demo2@example.com",
            "pass12345",
            name="Мария",
            surname="Петрова",
            phone="89004445566",
        )

        python_skill = Skill.objects.create(name="Python")
        django_skill = Skill.objects.create(name="Django")
        user1.skills.add(python_skill, django_skill)
        user2.skills.add(python_skill)

        project1 = Project.objects.create(
            name="TeamFinder App",
            description="Pet-проект для поиска команды",
            owner=user1,
            status=Project.STATUS_OPEN,
            github_url="https://github.com/example/teamfinder",
        )
        project1.participants.add(user1)

        project2 = Project.objects.create(
            name="ML Dashboard",
            description="Дашборд аналитики",
            owner=user2,
            status=Project.STATUS_OPEN,
        )
        project2.participants.add(user2)

        self.stdout.write(self.style.SUCCESS("Демо-данные созданы."))
        self.stdout.write("demo1@example.com / pass12345")
        self.stdout.write("demo2@example.com / pass12345")

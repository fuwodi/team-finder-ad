from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from users.avatar import generate_avatar_image
from users.managers import UserManager


class Skill(models.Model):
    name = models.CharField("Название", max_length=124)

    class Meta:
        ordering = ["name"]
        verbose_name = "навык"
        verbose_name_plural = "Навыки"

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("Email", unique=True)
    name = models.CharField("Имя", max_length=124)
    surname = models.CharField("Фамилия", max_length=124)
    avatar = models.ImageField("Аватар", upload_to="avatars/")
    phone = models.CharField("Телефон", max_length=12, blank=True, default="")
    github_url = models.URLField("GitHub", blank=True)
    about = models.TextField("О себе", max_length=256, blank=True)
    is_active = models.BooleanField("Активный", default=True)
    is_staff = models.BooleanField("Администратор", default=False)
    skills = models.ManyToManyField(
        Skill,
        blank=True,
        related_name="users",
        verbose_name="Навыки",
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    class Meta:
        ordering = ["id"]
        verbose_name = "пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.name} {self.surname}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new and not self.avatar:
            letter = self.name[0] if self.name else "?"
            self.avatar = generate_avatar_image(letter)
        super().save(*args, **kwargs)

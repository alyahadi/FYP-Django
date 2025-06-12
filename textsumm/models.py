# your_app/models.py

from django.conf import settings
from django.db import models


class TextSumm(models.Model):
    name        = models.CharField(max_length=255)
    text        = models.TextField(default="")
    image       = models.ImageField(upload_to="FYP Cover Images/")
    video       = models.URLField(blank=True, default="")
    lineage     = models.TextField(default="")
    conversion  = models.TextField(default="")
    persecution = models.TextField(default="")
    hijrah      = models.TextField(default="")
    battle      = models.TextField(default="")
    trait       = models.TextField(default="")
    death       = models.TextField(default="")

    def __str__(self):
        return self.name


class Note(models.Model):
    """
    A user’s note/reflection attached to a particular TextSumm entry.
    """
    user       = models.ForeignKey(
                    settings.AUTH_USER_MODEL,
                    on_delete=models.CASCADE,
                    related_name="notes"
                 )
    textsumm   = models.ForeignKey(
                    TextSumm,
                    on_delete=models.CASCADE,
                    related_name="notes"
                 )
    content    = models.TextField()
    is_public  = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Note/Reflection"
        verbose_name_plural = "Notes & Reflections"

    def __str__(self):
        excerpt = self.content[:30].replace("\n", " ")
        return f"{self.user.username} → {self.textsumm.name}: {excerpt}…"

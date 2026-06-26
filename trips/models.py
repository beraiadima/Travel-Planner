from django.db import models

class TravelProject(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    is_completed = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProjectPlace(models.Model):
    project = models.ForeignKey(
        TravelProject, on_delete=models.CASCADE, related_name="places"
    )
    external_id = models.IntegerField()
    title = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)
    is_visited = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("project", "external_id")

    def __str__(self):
        return f"{self.project.name} — {self.title}"
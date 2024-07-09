from django.db import models


class TechDocSource(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class TechDocCategory(models.Model):
    name = models.CharField(max_length=200)
    source = models.ForeignKey(TechDocSource, on_delete=models.CASCADE, related_name='categories')

    class Meta:
        unique_together = ['name', 'source']

    def __str__(self):
        return f"{self.source.name} - {self.name}"


class TechDoc(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField(max_length=400)
    pub_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(TechDocCategory, on_delete=models.CASCADE, related_name='docs')

    def __str__(self):
        return self.title



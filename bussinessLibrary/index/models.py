from django.db import models


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=128,unique=True)
    url = models.URLField(max_length=200)
    time = models.DateTimeField()
    sourceId = models.IntegerField( default=-1 )

    def __str__(self):
        return self.name
    class Meta:
        ordering = ["time"]
        verbose_name = "项目"
        verbose_name_plural = "项目"


# class LastProject(models.Model):
#     name = models.CharField(max_length=128, unique=True)
#     sourceId = models.IntegerField(unique=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         ordering = ["sourceId"]
#         verbose_name = "最新项目"
#         verbose_name_plural = "最新项目"


class KeyWord(models.Model):
    keyword = models.CharField(max_length=128,unique=True)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ["keyword"]
        verbose_name = "关键词"
        verbose_name_plural = "关键词"


class Email(models.Model):
    #改了一下
    address = models.EmailField( max_length=128,unique=True,primary_key=True,null=False)
    annotation = models.CharField(max_length=128,unique=True)
    class Meta:
        verbose_name = "邮箱"
        verbose_name_plural="邮箱"



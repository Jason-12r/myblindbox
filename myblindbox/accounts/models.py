from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # 自定义用户模型
    gender_choices = [
        ('M', '男'),
        ('F', '女')
    ]
    weight_choices = [
        ('thin', '瘦'),
        ('normal', '正常'),
        ('fat', '胖')
    ]
    height_choices = [
        ('short', '矮'),
        ('average', '一般'),
        ('tall', '高')
    ]

    # 这些字段的最大长度调整为适应可能的最大值
    gender = models.CharField(max_length=1, choices=gender_choices, default='M')
    weight = models.CharField(max_length=10, choices=weight_choices, default='normal')  # 修改为更大的长度
    height = models.CharField(max_length=10, choices=height_choices, default='average')  # 修改为更大的长度

    # 使用 related_name 避免与 auth.User 的字段冲突
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # 修改 related_name，避免与 auth.User.groups 冲突
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_user_permissions',  # 修改 related_name，避免与 auth.User.user_permissions 冲突
        blank=True
    )

    def __str__(self):
        return self.username

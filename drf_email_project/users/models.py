from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid

# Create your models here.


class EmailUser(AbstractUser):
    ''' Email account fields '''

    def __init__(self, *args, **kwargs):
        AbstractUser.__init__(self, *args, **kwargs)
    id = models.UUIDField(_("用户ID"), primary_key=True, default=uuid.uuid4)
    username = models.CharField(
        _("用户名"), unique=True, max_length=20, blank=True, null=True)
    password = models.CharField(
        _("用户密码"), max_length=100, blank=True)
    avatar = models.ImageField(_("user's avater"), upload_to="avatar/",
                               default="", null=True, blank=True)
    email = models.EmailField(_("用户邮箱"), unique=True, max_length=255)
    is_verify = models.BooleanField(_("是否验证"), default=False)
    is_active = models.BooleanField(_("是否激活"), default=False)
    created_at = models.DateTimeField(_("创建时间"), auto_now_add=True)
    updated_at = models.DateTimeField(_("更新时间"), auto_now_add=True)

    class Meta:
        verbose_name = "邮箱用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

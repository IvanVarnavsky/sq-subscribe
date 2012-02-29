# -*- coding: utf-8 -*-
from sq_user.baseuser.models import BaseUser


class User(BaseUser):
    pass

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

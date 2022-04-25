from django.db import models
from datetime import datetime
from datetime import date


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_flag = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class TGenerateTrackingNumber(models.Model):
    id = models.IntegerField(blank=True, auto_created=True, primary_key=True)
    env = models.CharField(blank=True, max_length=255)
    product = models.CharField(blank=True, max_length=255)
    tracking_number = models.CharField(blank=True, max_length=255)
    create_user = models.CharField(blank=True, max_length=255)
    create_time = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        managed = False
        db_table = 't_generate_tracking_number'

    def to_dict(self):
        """重写model_to_dict()方法转字典"""
        opts = self._meta
        data = {}
        for f in opts.concrete_fields:
            value = f.value_from_object(self)
            if isinstance(value, datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(f, models.FileField):
                value = value.url if value else None
            data[f.name] = value
        return data


class TUrlManage(models.Model):
    id = models.IntegerField(blank=True, primary_key=True)
    name = models.CharField(blank=True, max_length=255, null=True)
    env = models.CharField(blank=True, max_length=255, null=True)
    url = models.CharField(blank=True, max_length=255, null=True)
    path = models.CharField(blank=True, max_length=255, null=True)
    port = models.CharField(blank=True, max_length=255, null=True)

    class Meta:
        managed = False
        db_table = 't_url_manage'

    def to_dict(self):
        """重写model_to_dict()方法转字典"""
        opts = self._meta
        data = {}
        for f in opts.concrete_fields:
            value = f.value_from_object(self)
            if isinstance(value, datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(f, models.FileField):
                value = value.url if value else None
            data[f.name] = value
        return data


class TValidationResult(models.Model):
    id = models.IntegerField(blank=True, auto_created=True, primary_key=True)  # Field name made lowercase.
    env = models.CharField(blank=True, max_length=255, null=True)
    test_case_num = models.IntegerField(blank=True, null=True)
    success_num = models.IntegerField(blank=True, null=True)
    failed_num = models.IntegerField(blank=True, null=True)
    pass_rate = models.CharField(blank=True, max_length=255, null=True)
    result = models.CharField(blank=True, max_length=255, null=True)
    result_file_name = models.CharField(blank=True, max_length=255, null=True)
    create_user = models.CharField(blank=True, max_length=255, null=True)
    create_time = models.TextField(blank=True, max_length=255, null=True)
    is_active = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_validation_result'

    def to_dict(self):
        """重写model_to_dict()方法转字典"""
        opts = self._meta
        data = {}
        for f in opts.concrete_fields:
            value = f.value_from_object(self)
            if isinstance(value, datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(f, models.FileField):
                value = value.url if value else None
            data[f.name] = value
        return data


class TValidationTestCase(models.Model):
    id = models.IntegerField(blank=True, auto_created=True, primary_key=True)  # Field name made lowercase.
    desc = models.CharField(blank=True, max_length=255, null=True)
    ele = models.CharField(blank=True, max_length=255, null=True)
    service = models.CharField(blank=True, max_length=255, null=True)
    request_data = models.CharField(blank=True, max_length=2550, null=True)
    check_type = models.CharField(blank=True, max_length=255, null=True)
    exp_data = models.CharField(blank=True, max_length=255, null=True)
    check_data = models.CharField(blank=True, max_length=255, null=True)
    create_user = models.CharField(blank=True, max_length=255, null=True)
    create_time = models.TextField(blank=True, max_length=255, null=True)
    is_active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 't_validation_test_case'

    def to_dict(self):
        """重写model_to_dict()方法转字典"""
        opts = self._meta
        data = {}
        for f in opts.concrete_fields:
            value = f.value_from_object(self)
            if isinstance(value, datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(f, models.FileField):
                value = value.url if value else None
            data[f.name] = value
        return data


class TCheckSql(models.Model):
    id = models.IntegerField(blank=True, auto_created=True, primary_key=True)
    request_file = models.CharField(blank=True, max_length=255, null=True)
    result_file = models.CharField(blank=True, max_length=255, null=True)
    data_len = models.IntegerField()
    aq_status = models.CharField(blank=True, max_length=255, null=True)
    rdc_status = models.CharField(blank=True, max_length=255, null=True)
    version_time = models.DateField()
    create_time = models.DateTimeField()
    create_user = models.CharField(blank=True, max_length=255, null=True)
    is_active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 't_check_sql'

    def to_dict(self):
        """重写model_to_dict()方法转字典"""
        opts = self._meta
        data = {}
        for f in opts.concrete_fields:
            value = f.value_from_object(self)
            if isinstance(value, datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            if isinstance(value, date):
                value = value.strftime('%Y-%m-%d')
            elif isinstance(f, models.FileField):
                value = value.url if value else None
            data[f.name] = value
        return data

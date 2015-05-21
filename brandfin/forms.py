from django.forms import ModelForm, Field, ValidationError
from django.db import DatabaseError
from django import forms

from models import Query, MSG_FAILED_BLACKLIST, DataConnection, ReportTemplate


_ = lambda x: x


class SqlField(Field):
    def validate(self, value):
        """
        Ensure that the SQL passes the blacklist and executes. Execution check is skipped if params are present.

        :param value: The SQL for this Query model.
        """

        query = Query(sql=value)

        error = MSG_FAILED_BLACKLIST if not query.passes_blacklist() else None

        if not error and not query.available_params():
            try:
                query.try_execute()
            except DatabaseError as e:
                error = str(e)

        if error:
            raise ValidationError(
                _(error),
                code="InvalidSql"
            )


class QueryForm(ModelForm):
    sql = SqlField()

    def clean(self):
        if self.instance and self.data.get('created_by_user', None):
            self.cleaned_data['created_by_user'] = self.instance.created_by_user
        return super(QueryForm, self).clean()

    @property
    def created_by_user_email(self):
        return self.instance.created_by_user.email if self.instance.created_by_user else '--'

    @property
    def created_by_user_id(self):
        return self.instance.created_by_user.id if self.instance.created_by_user else '--'

    class Meta:
        model = Query
        daily_run = forms.BooleanField(initial=False)
        fields = ['title', 'sql', 'description', 'created_by_user', 'daily_run']

class TemplateForm(ModelForm):
    sql = SqlField()

    def clean(self):
        if self.instance and self.data.get('created_by_user', None):
            self.cleaned_data['created_by_user'] = self.instance.created_by_user
        return super(TemplateForm, self).clean()

    @property
    def created_by_user_email(self):
        return self.instance.created_by_user.email if self.instance.created_by_user else '--'

    @property
    def created_by_user_id(self):
        return self.instance.created_by_user.id if self.instance.created_by_user else '--'

    class Meta:
        model = ReportTemplate
        fields = ['title', 'sql', 'description', 'created_by_user']


class DataConnectionForm(forms.ModelForm):
    class Meta:
        model = DataConnection
        widgets = {
            'password': forms.PasswordInput(),
        }
        fields = "__all__"

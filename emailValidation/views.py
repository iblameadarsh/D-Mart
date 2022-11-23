import pandas as pd
from django.views.generic import FormView, ListView, View
from emailValidation.models import *
from emailValidation.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from D_Mart.db_connect import DATABASE as MONGO_DATABASE
from datetime import *
from Users.models import ActivityLogs


class EmailValidationView(LoginRequiredMixin, FormView):
    template_name = 'emailValidation/emailValidForm.html'
    form_class = EmailExportModelform
    success_url = '/tools/email-validation-task-list/'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        obj.check_input_file()
        return super(EmailValidationView, self).form_valid(form)


class EmailTaskListView(LoginRequiredMixin, ListView):
    model = ValidEmailExport
    queryset = ValidEmailExport.objects.order_by('-created_at')
    context_object_name = 'ValidEmailExport'
    template_name = 'emailValidation/fromView.html'

    def get_context_data(self, **kwargs):
        context = super(EmailTaskListView, self).get_context_data()
        context['ValidEmailExport'] = context['ValidEmailExport'].filter(user=self.request.user)
        return context


class EmailFinalExport(View):

    def __init__(self, **kwargs):
        self.DBOBJ = MONGO_DATABASE()

    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def get(self, request, task_id, **kwargs):
        # file_name = "Verified_Emails_REPORT" + "_" + str(datetime.now()).replace(" ", "_") + {} +".csv"
        task = ValidEmailExport.objects.get(pk=int(task_id))
        taskName = str(task.task_name)
        file_name = f'{taskName}-{task_id}-{str(datetime.now()).replace(" ", "_")}.csv'
        df = pd.DataFrame(list(self.DBOBJ.email_validation_exports.find({
            'task id': int(task_id)})))
        df = df.where(pd.notnull(df), '')
        fdf = df.drop(['_id', 'task id', 'message', 'Http status code'], axis=1)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}'.format(file_name)
        fdf.to_csv(path_or_buf=response, index=False)
        logobj = ActivityLogs()
        logobj.log_type = 'file_export'
        logobj.description = "File: {} Exported From Email Validations Export Feature".format(file_name)
        logobj.user = request.user
        logobj.save()
        return response


def download_template(request):
    if request.method == 'GET':
        temp = {'name': '', 'email': ''}
        df = pd.DataFrame(temp, index=range(0))
        file_name = "template.csv"
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}'.format(file_name)
        df.to_csv(path_or_buf=response, index=False, encoding='utf-8')
        logobj = ActivityLogs()
        logobj.log_type = 'file_export'
        logobj.description = "File: {} Exported From Email Validations Export Feature".format(file_name)
        logobj.user = request.user
        logobj.save()
        return response


# class ExportTemplateFile(View):
#
#     def dispatch(self, request, *args, **kwargs):
#         return super(self.__class__, self).dispatch(self, request, *args, **kwargs)
#
#     def get(self, request, **kwargs):
#         temp = {'email': ''}
#         tdf = pd.DataFrame(temp, index=range(1000))
#         file_name = "template.csv"
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
#         tdf.to_csv(path_or_buf=response)
#         return response


from django.contrib import admin
from .models import Student, Campus,Cursus, Faculty, Employee, Message, Job

admin.site.register(Student)
admin.site.register(Employee)
admin.site.register(Campus)
admin.site.register(Cursus)
admin.site.register(Faculty)
admin.site.register(Message)
admin.site.register(Job)

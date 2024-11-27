from django.db import models


#DB fetching for instructors data
class InstructorData(models.Model):
    instructor_id = models.AutoField(primary_key=True)
    college_id = models.IntegerField(default=0)
    last_name = models.CharField(max_length=255, default="")
    first_name = models.CharField(max_length=255, default="")
    middle_initial = models.CharField(max_length=1, null=True, blank=True)
    employment_type = models.CharField(
        max_length=10, 
        choices=[('regular', 'Regular'), ('cos', 'COS')], 
        default='regular'
    )
    qualified_course = models.JSONField(default=dict)  
    availability_days = models.JSONField(default=list)  
    availability_times = models.JSONField(default=list)  

    class Meta:
      db_table = 'instructors_data'

    def __str__(self):
        return f"{self.last_name}, {self.first_name} {self.middle_initial or ''}"

#DB fetching for program ids
class Program(models.Model):
    program_id = models.AutoField(primary_key=True)
    college_id = models.IntegerField()
    program_code = models.TextField(null=True, blank=True)
    program_name = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'Program'  

    def __str__(self):
        return f"{self.program_name} ({self.program_code})"

#DB fetching for courses / semester / credit_hours
class InstructorCourse(models.Model):
    course_id = models.AutoField(primary_key=True)
    instructor_id = models.IntegerField(default=0)
    program_id = models.IntegerField(default=0)
    course_code = models.TextField(null=True, blank=True)
    course_name = models.TextField(null=True, blank=True)
    department = models.TextField(null=True, blank=True)
    credit_hours = models.IntegerField(null=True, blank=True)
    prerequisites = models.JSONField(null=True, blank=True)
    school_year = models.TextField(null=True, blank=True)
    semester = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'instructor_course'  

    def __str__(self):
        return f"{self.course_name} ({self.course_code}) - Semester {self.semester}"
from django.db import models
from authentication.models import User
from django_ckeditor_5.fields import CKEditor5Field


class SchoolYear(models.Model):

    class Meta:
        verbose_name = "School Year"
        verbose_name_plural = "School Years"

    school_year = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.school_year
    
class Task(models.Model):

    class TaskStatus(models.TextChoices):
        PENDING = "PENDING","PENDING"
        VERIFIED = "VERIFIED","VERIFIED"

    BASE_STATUS = TaskStatus.PENDING

    class TaskPrincipleType(models.TextChoices):
        LEADERSHIP = "LEADERSHIP","LEADERSHIP"
        CURRICULUM_LEARNING = "CURRICULUM & LEARNING","CURRICULUM & LEARNING"
        ACCOUNTABILITY = "ACCOUNTABILITY","ACCOUNTABILITY"
        MANAGEMENT = "RESOURCE MANAGEMENT","RESOURCE MANAGEMENT"


    task_name = models.CharField(max_length=255)
    task_description = CKEditor5Field(max_length=1500,config_name="extends")
    assigned_to = models.ForeignKey(User,on_delete=models.CASCADE,related_name="assgined_to",default="",limit_choices_to={'user_role':User.Role.MEMBER})
    assigned_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="assgined_by",default="")
    is_active = models.BooleanField(default=True)
    task_status = models.BooleanField(default=False)
    status = models.CharField(choices=TaskStatus.choices,default=BASE_STATUS,max_length=255)
    task_due = models.DateField(null=True)
    principle = models.CharField(choices=TaskPrincipleType.choices,default="",max_length=255)
    current_sy = models.ForeignKey(SchoolYear,on_delete=models.SET_NULL,null=True)
    task_date_added = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        get_latest_by = 'task_date_added'

    def __str__(self) -> str:
        return str(self.task_name)
    
class Document(models.Model):

    class Meta:
        verbose_name = "Task Document"
        verbose_name_plural = "Task Documents"

    document = models.FileField(upload_to="document/")
    document_name = models.CharField(max_length=255,null=True)
    document_type = models.CharField(max_length=100,null=True)
    document_size = models.CharField(max_length=255,null=True)
    download_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    uploaded_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    task = models.ForeignKey(Task,on_delete=models.SET_NULL,null=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return str(self.uploaded_by.username)

class AccessRate(models.Model):

    class Meta:
        verbose_name = "Enrollment Rate Score"
        verbose_name_plural = "Enrollment Rate Scores"

    school_year_one = models.OneToOneField('SchoolYear',on_delete=models.CASCADE,related_name="school_year_one",default="")
    school_year_two = models.OneToOneField('SchoolYear',on_delete=models.CASCADE,related_name="school_year_two",default="")
    school_year_three = models.OneToOneField('SchoolYear',on_delete=models.CASCADE,related_name="school_year_three",default="")
    enrollment_increase_one = models.FloatField(max_length=9)
    enrollment_increase_two = models.FloatField(max_length=9)
    enrollment_increase_three = models.FloatField(max_length=9)
    percent_increase_two = models.FloatField(max_length=10)
    percent_increase_three = models.FloatField(max_length=10)
    average = models.FloatField(max_length=100)
    final_result = models.FloatField()
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return str(self.date_added)

class Efficiency(models.Model):

    class Meta:
        verbose_name = "Efficiency Score"
        verbose_name_plural = "Efficiency Scores"

    drop_school_year_one = models.ForeignKey('SchoolYear',on_delete=models.CASCADE,related_name="drop_school_year_one",default="")
    drop_school_year_two = models.ForeignKey('SchoolYear',on_delete=models.CASCADE,related_name="drop_school_year_two",default="")
    drop_school_year_three = models.ForeignKey('SchoolYear',on_delete=models.CASCADE,related_name="drop_school_year_three",default="")
    drop_dropoutrate_one = models.FloatField(max_length=9)
    drop_dropoutrate_two = models.FloatField(max_length=9)
    drop_dropoutrate_three = models.FloatField(max_length=9)
    drop_percent_increase_two = models.FloatField(max_length=10)
    drop_percent_increase_three = models.FloatField(max_length=10)
    drop_average = models.FloatField(max_length=10)
    dropout_base_line_status = models.IntegerField(null=True,blank=True)
    drop_percent_decrease = models.FloatField(max_length=10)

    graduation_school_year_one = models.ForeignKey('SchoolYear',on_delete=models.CASCADE,related_name="graduation_school_year_one",default="")
    graduation_school_year_two = models.ForeignKey('SchoolYear',on_delete=models.CASCADE,related_name="graduation_school_year_two",default="")
    graduation_school_year_three = models.ForeignKey('SchoolYear',on_delete=models.CASCADE,related_name="graduation_school_year_three",default="")
    graduation_rate_one = models.FloatField(max_length=9)
    graduation_rate_two = models.FloatField(max_length=9)
    graduation_rate_three = models.FloatField(max_length=9)
    graduation_rate_average = models.FloatField(max_length=9)
    graduation_increase_per_two = models.FloatField(max_length=9)
    graduation_increase_per_three = models.FloatField(max_length=9)
    graduation_increase_average = models.FloatField(max_length=9)
    graduation_base_line_status = models.IntegerField(null=True,blank=True)    

    promotion_school_year_one = models.ForeignKey('SchoolYear',on_delete=models.CASCADE,related_name="promotion_school_year_one",default="")
    promotion_school_year_two = models.ForeignKey('SchoolYear',on_delete=models.CASCADE,related_name="promotion_school_year_two",default="")
    promotion_school_year_three = models.ForeignKey('SchoolYear',on_delete=models.CASCADE,related_name="promotion_school_year_three",default="")
    promotion_rate_one = models.CharField(max_length=9)
    promotion_rate_two = models.CharField(max_length=9)
    promotion_rate_three = models.CharField(max_length=9)
    promotion_rate_average = models.CharField(max_length=9)
    promotion_increase_per_two = models.CharField(max_length=9)
    promotion_increase_per_three = models.CharField(max_length=9)
    promotion_increase_average = models.CharField(max_length=9)
    promotion_base_line_status = models.IntegerField(null=True,blank=True)
    final_result = models.FloatField()    
    sub_total = models.TextField(null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.date_added)

class QualityRate(models.Model):

    class Meta:
        verbose_name = "NAT/Quality Score"
        verbose_name_plural = "NAT/Quality Scores"

    quality_school_year_one = models.ForeignKey('SchoolYear',on_delete=models.CASCADE,related_name="quality_school_year_one",limit_choices_to={'is_active':True},default="")
    quality_school_year_two = models.ForeignKey('SchoolYear',on_delete=models.CASCADE,related_name="quality_school_year_two",limit_choices_to={'is_active':True},default="")
    quality_school_year_three = models.ForeignKey('SchoolYear',on_delete=models.CASCADE,related_name="quality_school_year_three",limit_choices_to={'is_active':True},default="")

    quality_rate_one = models.CharField(max_length=9)
    quality_rate_two = models.CharField(max_length=9)
    quality_rate_three = models.CharField(max_length=9)
    quality_rate_average = models.CharField(max_length=9)
    quality_rate_two_percentage = models.CharField(max_length=9)
    quality_rate_three_percentage = models.CharField(max_length=9)
    quality_rate_average_percentage = models.CharField(max_length=9)
    quality_final_result = models.FloatField()
    quality_date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.quality_date_added)
    
class Rating(models.Model):

    class Meta:
        verbose_name = "Rating Score"
        verbose_name_plural = "Rating Scores"

    access_id = models.ForeignKey(AccessRate,on_delete=models.CASCADE,null=True,blank=True)
    efficiency_id = models.ForeignKey(Efficiency,on_delete=models.CASCADE,null=True,blank=True)
    quality_id = models.ForeignKey(QualityRate,on_delete=models.CASCADE,null=True,blank=True)
    leadership_id = models.ForeignKey('AssessmentScore',on_delete=models.CASCADE,related_name="leadership_id",null=True,blank=True)
    curriculum_id = models.ForeignKey('AssessmentScore',on_delete=models.CASCADE,related_name="curriculum_id",null=True,blank=True)
    accountability_id = models.ForeignKey('AssessmentScore',on_delete=models.CASCADE,related_name="accountability_id",null=True,blank=True)
    management_id = models.ForeignKey('AssessmentScore',on_delete=models.CASCADE,related_name="management_id",null=True,blank=True)
    performance_id = models.ForeignKey('ImprovementScore',on_delete=models.CASCADE,related_name="performance_sbm_id",null=True,blank=True)
    sbm_assessment_id = models.ForeignKey('ImprovementScore',on_delete=models.CASCADE,related_name="sbm_assessment_id",null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.date_added)
    
class AssessmentScore(models.Model):

    class Meta:
        verbose_name = "Assessment Score"
        verbose_name_plural = "Assessment Scores"

    WEIGHTS = (
        ('30','30%'),
        ('25','25%'),
        ('15','15%'),
    )

    class AssessmentPrincipleType(models.TextChoices):
        LEADERSHIP = "LEADERSHIP","LEADERSHIP"
        CURRICULUM_LEARNING = "CURRICULUM & LEARNING","CURRICULUM & LEARNING"
        ACCOUNTABILITY = "ACCOUNTABILITY","ACCOUNTABILITY"
        MANAGEMENT = "RESOURCE MANAGEMENT","RESOURCE MANAGEMENT"

    principle = models.CharField(choices=AssessmentPrincipleType.choices,default="",max_length=255)
    weight = models.TextField(choices=WEIGHTS,max_length=255,default="")
    principle_score = models.FloatField()
    cumulative_score = models.FloatField()
    result = models.FloatField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.principle

class ImprovementScore(models.Model):

    class Meta:
        verbose_name = "Improvement Score"
        verbose_name_plural = "Improvement Scores"

    WEIGHTS = (
        ('60','60%'),
        ('40','40%')
    )

    AREAS = (
        ('Performance Improvement','Performance Improvement'),
        ('SBM Assessment Score (DOD)','SBM Assessment Score (DOD)')
    )


    area = models.TextField(choices=AREAS,max_length=255,default="")
    weight = models.TextField(choices=WEIGHTS,max_length=255,default="")
    rating = models.FloatField()
    result = models.FloatField()


    def __str__(self) -> str:
        return self.area

class PerformanceImprovementInterpretation(models.Model):

    class Meta:
        verbose_name = "Performance Improvement Interpretation"
        verbose_name_plural = "Performance Improvement Interpretations"

    class Description(models.TextChoices):
        GOOD = "GOOD","GOOD"
        BETTER = "BETTER","BETTER"
        BEST = "BEST","BEST"
    
    
    access = models.ForeignKey(AccessRate,on_delete=models.CASCADE)
    efficiency = models.ForeignKey(Efficiency,on_delete=models.CASCADE)
    quality = models.ForeignKey(QualityRate,on_delete=models.CASCADE)
    rating = models.FloatField()
    description = models.TextField(choices=Description.choices,default="",max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Performance Improvement {str(self.rating)}'
    

    def save(self, *args,**kwargs):
        if self.rating <= 1.49:
            self.description = self.Description.GOOD
        elif 1.50 <= self.rating <= 2.49:
            self.description = self.Description.BETTER
        elif self.rating >= 2.50:
            self.description = self.Description.BEST
        return super().save(*args,**kwargs)
    
class AssessmentScoreInterpretation(models.Model):

    class Meta:
        verbose_name = "Assessment Score Interpretation"
        verbose_name_plural = "Assessment Score Interpretations"

    leadership = models.ForeignKey(AssessmentScore,on_delete=models.CASCADE,related_name="leadership")
    curriculum = models.ForeignKey(AssessmentScore,on_delete=models.CASCADE,related_name="curriculum")
    accountability = models.ForeignKey(AssessmentScore,on_delete=models.CASCADE,related_name="accountability")
    management = models.ForeignKey(AssessmentScore,on_delete=models.CASCADE,related_name="management")
    rating = models.FloatField()
    description = models.TextField(choices=PerformanceImprovementInterpretation.Description.choices,default="",max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Performance Improvement {str(self.rating)}'
    

    def save(self, *args,**kwargs):
        if self.rating <= 1.49:
            self.description = PerformanceImprovementInterpretation.Description.GOOD
        elif 1.50 <= self.rating <= 2.49:
            self.description = PerformanceImprovementInterpretation.Description.BETTER
        elif self.rating >= 2.50:
            self.description = PerformanceImprovementInterpretation.Description.BEST
        return super().save(*args,**kwargs)

class FinalRatingInterpretation(models.Model):

    class Meta:
        verbose_name = "Final Rating Interpretation"
        verbose_name_plural = "Final Rating Interpretations"

    class Description(models.TextChoices):
        DEVELOPING = "DEVELOPING (LEVEL) I","DEVELOPING (LEVEL) I"
        MATURING = "MATURING (LEVEL) II","MATURING (LEVEL) II"
        ADVANCED = "ADVANCED (LEVEL) III","ADVANCED (LEVEL) III"

    performance = models.ForeignKey(ImprovementScore,on_delete=models.CASCADE,related_name="performance")
    assessment = models.ForeignKey(ImprovementScore,on_delete=models.CASCADE,related_name="assessment")
    rating = models.FloatField()
    description = models.TextField(choices=Description.choices,max_length=20,default="")
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return f'Final rating {str(self.rating)}'
    

    def save(self, *args,**kwargs):
        if self.rating <= 1.49:
            self.description = self.Description.DEVELOPING
        elif 1.50 <= self.rating <= 2.49:
            self.description = self.Description.MATURING
        elif self.rating >= 2.50:
            self.description = self.Description.ADVANCED
        return super().save(*args,**kwargs)





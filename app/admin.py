from django.contrib import admin
from app.models import Document,Task,AccessRate,QualityRate,SchoolYear,Efficiency,Rating,AssessmentScore,ImprovementScore,PerformanceImprovementInterpretation,AssessmentScoreInterpretation,FinalRatingInterpretation

class DocumentAdmin(admin.ModelAdmin):
    list_display = ("task","uploaded_by","document_name","document_type","document_size","date_uploaded",)
    list_filter = ("task","document_type","date_uploaded",)
    list_max_show_all = 6


class TaskAdmin(admin.ModelAdmin):
    list_display = ("task_name","assigned_by","assigned_to","task_due","current_sy","task_date_added",)
    list_filter = ("task_name","assigned_by","assigned_to","task_due","task_date_added",)
    list_editable = ("current_sy",)
    list_max_show_all = 6

class SchoolYearAdmin(admin.ModelAdmin):
    list_display = ("school_year","is_active","date_added",)
    list_editable = ("is_active",)
    list_filter = ("is_active",)
    list_max_show_all = 6



class SchoolYearAdmin(admin.ModelAdmin):
    list_display = ("school_year","is_active","date_added",)
    list_editable = ("is_active",)
    list_filter = ("is_active","date_added",)
    list_per_page = 6

class AccessRateAdmin(admin.ModelAdmin):
    list_display = ("school_year_one","school_year_two","school_year_three","enrollment_increase_one","enrollment_increase_two","enrollment_increase_three","average","final_result","date_added",)
    list_editable = ("enrollment_increase_one","enrollment_increase_two","enrollment_increase_three",)
    list_filter = ("date_added",)
    list_per_page = 6

admin.site.register(Document,DocumentAdmin)
admin.site.register(Task,TaskAdmin)
admin.site.register(AccessRate,AccessRateAdmin)
admin.site.register(QualityRate)
admin.site.register(Efficiency)
admin.site.register(Rating)
admin.site.register(AssessmentScore)
admin.site.register(ImprovementScore)
admin.site.register(SchoolYear,SchoolYearAdmin)



class PerformanceImprovementInterpretationAdmin(admin.ModelAdmin):
    list_display = ("access","rating","description","date_added")
    list_per_page = 6

admin.site.register(PerformanceImprovementInterpretation,PerformanceImprovementInterpretationAdmin)


class AssessmentInterpretationAdmin(admin.ModelAdmin):
    list_display = ("leadership","curriculum","accountability","management","rating","description","date_added",)
    list_per_page = 6

admin.site.register(AssessmentScoreInterpretation,AssessmentInterpretationAdmin)


class FinalRatingAdmin(admin.ModelAdmin):
    list_display = ("performance","assessment","rating","description","date_added",)
    list_per_page = 6

admin.site.register(FinalRatingInterpretation,FinalRatingAdmin)


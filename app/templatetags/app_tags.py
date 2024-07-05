from django import template

register = template.Library()

@register.filter(name='convert_bytes_to_mb')
def convert_bytes_to_mb(bytes_size):
    return int(bytes_size) / (1024.0 ** 2)

@register.simple_tag
def performance_result(assessment_result,efficiency_result,quality_result):
    result = float(assessment_result) + float(efficiency_result) + float(quality_result)
    return round(result,2)


@register.simple_tag
def assessment_result(leadership_result,curriculum_result,accountability_result,management_result):
    result = float(leadership_result) + float(curriculum_result) + float(accountability_result) + float(management_result)
    return round(result,2)


@register.simple_tag
def final_rating_result(performance,assessment):
    result = float(performance) + float(assessment)
    return round(result,2)
from django.shortcuts import get_object_or_404

def get_object_or_none(query, **kwargs):
    try:
        return get_object_or_404(query, **kwargs)
    except:
        return None
    
month_list = (
    ('january',1),
)
def get_month(string):
    return dict(month_list)[str(string).lower()]
    
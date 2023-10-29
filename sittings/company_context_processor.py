from .models import Company

# we use context processor to return data in all pages

def get_company_data(request):
    data = Company.objects.last()
    return {'company_data': data}
from django.http import JsonResponse

def home(request):
    return JsonResponse({"message":"Welcome to AirIndia"})

def privacyPolicy(request):
    return JsonResponse({"message":"Privacy Policy"})

def termsAndServices(request):
    return JsonResponse({"message":"Terms and Services"})

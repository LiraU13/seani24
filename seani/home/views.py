from django.shortcuts import redirect, render

# Create your views here.
def home(request):
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return redirect('admin:index')
        else:
            return redirect('exam:home')
    return render(request, 'home/home.html')
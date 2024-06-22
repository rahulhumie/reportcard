from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Sum, Q, F, Window
from django.db.models.functions import Rank
from .models import Receipe, Student, SubjectMarks
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def receipies(request):
    if request.method == 'POST':
        recipe_name = request.POST.get('recipe_name')
        recipe_description = request.POST.get('recipe_description')
        recipe_image = request.FILES.get('recipe_image')

        # Debugging output to check the contents of the request
        print("POST data:", request.POST)
        print("FILES data:", request.FILES)

        # Ensure that the file is being processed correctly
        if recipe_image:
            Receipe.objects.create(
                recipe_name=recipe_name,
                recipe_description=recipe_description,
                recipe_image=recipe_image
            )
            return redirect('/receipes')
    queryset = Receipe.objects.all()
    context = {'receipes': queryset}
    return render(request, 'receipies.html', context)

def delete_receipe(request, id):
    queryset = Receipe.objects.get(id=id)
    queryset.delete()
    return redirect('/receipes')

def update_receipe(request, id):
    queryset = get_object_or_404(Receipe, id=id)
    if request.method == 'POST':
        recipe_name = request.POST.get('recipe_name')
        recipe_description = request.POST.get('recipe_description')
        recipe_image = request.FILES.get('recipe_image')

        # Update the queryset object with the new data
        queryset.recipe_name = recipe_name
        queryset.recipe_description = recipe_description
        if recipe_image:
            queryset.recipe_image = recipe_image
        queryset.save()

        return redirect('/receipes')
    if request.GET.get('search'):
        Receipe.objects.filter(recipe_name__icontains=request.GET.get('search'))

    context = {'receipe': queryset}
    return render(request, 'update_receipe.html', context)

def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('Username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username)
        if user.exists():
            messages.info(request, "Username already exists")
            return redirect('/register')

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        user.set_password(password)
        user.save()
        messages.info(request, "Account created successfully")
        return redirect('register')

    return render(request, 'register.html')

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('/login')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Invalid password')
            return redirect('/login')
        else:
            login(request, user)
            return redirect('receipies')

    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect('/login')

def get_students(request):
    queryset = Student.objects.annotate(total_marks=Sum('studentmarks__marks'))

    if request.GET.get('search'):
        search = request.GET.get('search')
        queryset = queryset.filter(
            Q(student_name__icontains=search) |
            Q(student_age__icontains=search) |
            Q(student_email__icontains=search) |
            Q(department__department__icontains=search) |
            Q(student_id__student_id__icontains=search)
        )
    paginator = Paginator(queryset, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'report/students.html', {'queryset': page_obj})

def see_marks(request, student_id):
    student = get_object_or_404(Student, student_id__student_id=student_id)
    queryset = SubjectMarks.objects.filter(student=student)
    total_marks = queryset.aggregate(total=Sum('marks'))['total']

    # Compute the rank of the student based on total marks
    ranked_students = Student.objects.annotate(
        total_marks=Sum('studentmarks__marks')
    ).annotate(
        rank=Window(expression=Rank(), order_by=F('total_marks').desc())
    )

    student_rank = next((s.rank for s in ranked_students if s.student_id.student_id == student_id), None)

    return render(request, 'report/see_marks.html', {
        'student': student, 
        'queryset': queryset, 
        'total_marks': total_marks, 
        'rank': student_rank
    })

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

from .models import Classroom, Student
from .forms import ClassroomForm, SigninForm, SignupForm, StudentForm

def classroom_list(request):
	classrooms = Classroom.objects.all()
	context = {
		"classrooms": classrooms,
	}
	return render(request, 'classroom_list.html', context)


def classroom_detail(request, classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)
	students = Student.objects.filter(classroom=classroom).order_by('name','-exam_grade')
	# students.order_by('grade')
	context = {
		"classroom": classroom,
		"students": students,
	}
	return render(request, 'classroom_detail.html', context)


def classroom_create(request):
	form = ClassroomForm()
	if not request.user.is_authenticated:
		return redirect('signin')
	if request.method == "POST":
		form = ClassroomForm(request.POST, request.FILES or None)
		if form.is_valid():
			classroom = form.save(commit=False)
			classroom.teacher = request.user
			classroom.save()
			messages.success(request, "Successfully Created!")
			return redirect('classroom-list')
		print (form.errors)
	context = {
	"form": form,
	}
	return render(request, 'create_classroom.html', context)

	# Add Update and Delete buttons for every student, and remember that only the classroom’s teacher is allowed to
	# Create, Update and Delete a Student from this classroom. Keep in mind that the Create, Update and Delete buttons will
	#  only be visible to the classroom’s teacher. Also,
	# make sure that the url names for these actions are as follows student-create, student-update, student-delete.


def classroom_update(request, classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)
	form = ClassroomForm(instance=classroom)
	if request.method == "POST":
		form = ClassroomForm(request.POST, request.FILES or None, instance=classroom)
		if form.is_valid():
			form.save()
			messages.success(request, "Successfully Edited!")
			return redirect('classroom-list')
		print (form.errors)
	context = {
	"form": form,
	"classroom": classroom,
	}
	return render(request, 'update_classroom.html', context)


def classroom_delete(request, classroom_id):
	Classroom.objects.get(id=classroom_id).delete()
	messages.success(request, "Successfully Deleted!")
	return redirect('classroom-list')

def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.set_password(user.password)
            user.save()

            login(request, user)
            return redirect("classroom-list")
    context = {
        "form":form,
    }
    return render(request, 'signup.html', context)

def signin(request):
    form = SigninForm()
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect('classroom-list')
    context = {
        "form":form
    }
    return render(request, 'signin.html', context)

def signout(request):
    logout(request)
    return redirect("signin")


def student_create(request, classroom_id):
	classroom_obj = Classroom.objects.get(id=classroom_id)
	form = StudentForm()
	if not request.user==classroom_obj.teacher:
		return redirect('classroom_list')
	if request.method == "POST":
		form = StudentForm(request.POST)
		if form.is_valid():
			student_from = form.save(commit=False)
			student_from.classroom = classroom_obj
			student_from.save()
			messages.success(request, "Successfully Added!")
			return redirect('classroom-detail', classroom_obj.id)
		print (form.errors)
	context = {
	"form": form,
	"classroom": classroom_obj
	}
	return render(request, 'student_add.html', context)


def student_update(request,classroom_id,student_id):
	classroom_obj = Student.objects.get(id=student_id).classroom
	if not request.user==classroom_obj.teacher:
		return redirect('classroom_list')
	student = Student.objects.get(id=student_id)

	form = StudentForm(instance=student)
	if request.method == "POST":
		form = StudentForm(request.POST, instance=student)
		if form.is_valid():
			form.save()
			messages.success(request, "Successfully Edited!")
			return redirect('classroom-list')
		print (form.errors)
	context = {
	"form": form,
	"student": student,
	}
	return render(request, 'student_update.html', context)

def student_delete(request, classroom_id,student_id):
	classroom_obj = Student.objects.get(id=student_id).classroom
	if not request.user==classroom_obj.teacher:
		return redirect('classroom_list')
	Student.objects.get(id=student_id).delete()
	messages.success(request, "Successfully Deleted!")
	return redirect('classroom-list')

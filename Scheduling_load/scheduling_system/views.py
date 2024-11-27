from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from .models import InstructorData, InstructorCourse, Program
from .forms import ProgramForm  # Ensure you have a form for Program

def home(request):
    return render(request, 'instructors_frontend/index.html')  # Original home page

# Create teaching load page
def create_teaching_load(request):
    return render(request, 'instructors_frontend/create_load.html')  # New page for teaching load

def teaching_load(request):
    return render(request,'instructors_frontend/teaching_load.html')

def search_instructors(request):
    if request.method == "GET":
        query = request.GET.get('q', '').strip()  # Get the search query
        filter_type = request.GET.get('filter', 'ALL')  # Get the filter type (ALL, regular, cos)

        # Debugging: Print query and filter
        print(f"Search Query: {query}, Filter: {filter_type}")

        # Start with all instructors
        instructors = InstructorData.objects.all()

        # Apply filtering logic based on employment type
        if filter_type == 'REGULAR':
            instructors = instructors.filter(employment_type='REGULAR')
        elif filter_type == 'COS':
            instructors = instructors.filter(employment_type='COS')

        # Apply query if present
        if query:
            # Split the query into parts (split by spaces)
            name_parts = query.split()

            # Dynamically build the query filters based on the parts
            filter_query = Q()

            for part in name_parts:
                filter_query |= Q(first_name__icontains=part) | Q(middle_initial__icontains=part) | Q(last_name__icontains=part)

            instructors = instructors.filter(filter_query)

        # Debugging: Print the number of instructors fetched
        print(f"Found {instructors.count()} instructors matching the query.")

        # Prepare the response for the search (as JSON for AJAX)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Prepare the list of instructor details to return
            data = [
                {
                    'name': f"{instructor.first_name} {instructor.middle_initial or ''} {instructor.last_name}".strip(),
                    'instructor_id': instructor.instructor_id,
                    'employment_type': instructor.employment_type,
                    'qualified_course': instructor.qualified_course,
                }
                for instructor in instructors
            ]



            return JsonResponse({'results': data})

        # For non-AJAX request, render the instructor list template
        return render(request, 'instructors_frontend/teaching_load.html', {
            'instructors': instructors,
            'filter': filter_type,  # Pass the employment type filter to the template
            'query': query,  # Pass the search query to the template
        })

@csrf_exempt
def instructor_details(request):
    instructor_id = request.GET.get('id')
    instructor = InstructorData.objects.get(instructor_id=instructor_id)

    # Prepare the instructor details to return as JSON
    data = {
        'instructor_id': instructor.instructor_id,
        'name': f"{instructor.first_name} {instructor.middle_initial or ''} {instructor.last_name}".strip(),
        'employment_type': instructor.employment_type,
        'qualified_courses': instructor.qualified_course,
    }

    return JsonResponse(data)


# List instructor courses
def instructor_course_list(request):
    courses = InstructorCourse.objects.all()
    return render(request, 'teaching_load.html', {'courses': courses})

# Add a program
def add_program(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to the home page or a specific list
    else:
        form = ProgramForm()
    return render(request, 'teaching_load.html', {'form': form})

# Edit a program
def edit_program(request, pk):
    program = get_object_or_404(Program, pk=pk)
    if request.method == 'POST':
        form = ProgramForm(request.POST, instance=program)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProgramForm(instance=program)
    return render(request, 'teaching_load.html', {'form': form})

from django.shortcuts import render, redirect
from .models import Resume, Section

def create_resume(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        resume = Resume.objects.create(user=request.user, title=title)
        return redirect('edit_resume', resume_id=resume.id)
    return render(request, 'resume_builder/create_resume.html')

def edit_resume(request, resume_id):
    resume = Resume.objects.get(id=resume_id)
    if request.method == 'POST':
        resume.title = request.POST.get('title')
        resume.save()
        # Handle sections (not implemented here)
        return redirect('edit_resume', resume_id=resume.id)
    return render(request, 'resume_builder/edit_resume.html', {'resume': resume})
# from django.http import HttpResponse
# from django.template.loader import render_to_string
# #from weasyprint import HTML
# from .models import Resume

def resume_complete(request):
    pass
#     # Fetch the resume data
#     resume = Resume.objects.get(user=request.user)

#     # Render the resume into HTML
#     html_string = render_to_string('resume_builder/resume_pdf.html', {'resume': resume})

#     # Convert the HTML to a PDF
#     html = HTML(string=html_string)
#     pdf = html.write_pdf()

#     # Save the PDF file to the user's profile
#     resume.pdf.save(f'resume_{request.user.username}.pdf', ContentFile(pdf))

#     # Redirect to profile or show the generated PDF
#     return HttpResponse(pdf, content_type='application/pdf')

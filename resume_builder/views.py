# # views.py




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Resume
from .forms import ResumeForm
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem




@login_required
def resume_list(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'resume_builder/resume_list.html', {'resumes': resumes})

@login_required
def create_resume(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            return redirect('resume_list')
    else:
        form = ResumeForm()
    return render(request, 'resume_builder/create_resume.html', {'form': form})

@login_required
def edit_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            return redirect('resume_list')
    else:
        form = ResumeForm(instance=resume)
    return render(request, 'resume_builder/edit_resume.html', {'form': form})

@login_required
def delete_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    resume.delete()
    return redirect('resume_list')

@login_required
def view_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    return render(request, 'resume_builder/view_resume.html', {'resume': resume})


@login_required
def download_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Styles for the PDF
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Title'], fontSize=24, spaceAfter=12, textColor='#8B0000')
    subtitle_style = ParagraphStyle('TitleStyle', parent=styles['Title'], fontSize=12, spaceAfter=6)
    header_style = ParagraphStyle('HeaderStyle', parent=styles['Heading2'], fontSize=14, spaceAfter=6)
    body_style = ParagraphStyle('BodyStyle', parent=styles['BodyText'], fontSize=11, leading=14)
    bullet_style = ParagraphStyle('BulletStyle', parent=styles['BodyText'], fontSize=11, leftIndent=20, leading=14)

    # PDF Content
    content = []

    # Name Section
    name = Paragraph(f"<b>{resume.name}</b>", title_style)
    contact = Paragraph(f"\t\t {resume.email} • {resume.phone}", subtitle_style)
    content.extend([name, contact, Spacer(1, 12)])

    # Summary
    summary_header = Paragraph("Summary", header_style)
    summary_body = Paragraph(resume.summary, body_style)
    content.extend([summary_header, summary_body, Spacer(1, 12)])

    # Professional Experience
    experience_header = Paragraph("Professional Experience", header_style)
    experiences = []
    for exp in resume.experience.split("\n"):
        experiences.append(ListItem(Paragraph(exp, bullet_style)))
    experience_list = ListFlowable(experiences, bulletFontSize=10, leftIndent=20)
    content.extend([experience_header, experience_list, Spacer(1, 12)])

    # Education
    education_header = Paragraph("Education", header_style)
    educations=[]
    for ed in resume.education.split('\n'):
        educations.append(ListItem(Paragraph(ed,bullet_style)))
    education_body = ListFlowable(educations, bulletFontSize=10, leftIndent=20)
    content.extend([education_header, education_body, Spacer(1, 12)])

    # Skills
    skills_header = Paragraph("Additional Skills", header_style)
    skills = resume.skills.split(", ")
    skill_list = ListFlowable([ListItem(Paragraph(skill, bullet_style)) for skill in skills])
    content.extend([skills_header, skill_list])

    # Build PDF
    doc.build(content)

    # Return response
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="resume_{resume.id}.pdf"'
    return response



























# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from .models import Resume
# from .forms import ResumeForm
# from weasyprint import HTML
# from django.template.loader import render_to_string
# from django.http import HttpResponse

# @login_required
# def resume_list(request):
#     resumes = Resume.objects.filter(user=request.user)
#     return render(request, 'resume_builder/resume_list.html', {'resumes': resumes})

# @login_required
# def create_resume(request):
#     if request.method == 'POST':
#         form = ResumeForm(request.POST)
#         if form.is_valid():
#             resume = form.save(commit=False)
#             resume.user = request.user
#             resume.save()
#             return redirect('resume_list')
#     else:
#         form = ResumeForm()
#     return render(request, 'resume_builder/create_resume.html', {'form': form})

# @login_required
# def edit_resume(request, resume_id):
#     resume = get_object_or_404(Resume, id=resume_id, user=request.user)
#     if request.method == 'POST':
#         form = ResumeForm(request.POST, instance=resume)
#         if form.is_valid():
#             form.save()
#             return redirect('resume_list')
#     else:
#         form = ResumeForm(instance=resume)
#     return render(request, 'resume_builder/edit_resume.html', {'form': form})

# @login_required
# def delete_resume(request, resume_id):
#     resume = get_object_or_404(Resume, id=resume_id, user=request.user)
#     resume.delete()
#     return redirect('resume_list')

# @login_required
# def view_resume(request, resume_id):
#     resume = get_object_or_404(Resume, id=resume_id, user=request.user)
#     return render(request, 'resume_builder/view_resume.html', {'resume': resume})

# @login_required
# def download_resume(request, resume_id):
#     resume = get_object_or_404(Resume, id=resume_id, user=request.user)
#     html = render_to_string('resume_builder/resume_pdf.html', {'resume': resume})
#     pdf = HTML(string=html).write_pdf()
#     response = HttpResponse(pdf, content_type='application/pdf')
#     response['Content-Disposition'] = f'filename="resume_{resume.id}.pdf"'
#     return response
    
    


# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from .models import Resume
# from .forms import ResumeForm
# from django.http import HttpResponse
# from reportlab.pdfgen import canvas
# from io import BytesIO

# @login_required
# def resume_list(request):
#     resumes = Resume.objects.filter(user=request.user)
#     return render(request, 'resume_builder/resume_list.html', {'resumes': resumes})

# @login_required
# def create_resume(request):
#     if request.method == 'POST':
#         form = ResumeForm(request.POST)
#         if form.is_valid():
#             resume = form.save(commit=False)
#             resume.user = request.user
#             resume.save()
#             return redirect('resume_list')
#     else:
#         form = ResumeForm()
#     return render(request, 'resume_builder/create_resume.html', {'form': form})

# @login_required
# def edit_resume(request, resume_id):
#     resume = get_object_or_404(Resume, id=resume_id, user=request.user)
#     if request.method == 'POST':
#         form = ResumeForm(request.POST, instance=resume)
#         if form.is_valid():
#             form.save()
#             return redirect('resume_list')
#     else:
#         form = ResumeForm(instance=resume)
#     return render(request, 'resume_builder/edit_resume.html', {'form': form})

# @login_required
# def delete_resume(request, resume_id):
#     resume = get_object_or_404(Resume, id=resume_id, user=request.user)
#     resume.delete()
#     return redirect('resume_list')

# @login_required
# def view_resume(request, resume_id):
#     resume = get_object_or_404(Resume, id=resume_id, user=request.user)
#     return render(request, 'resume_builder/view_resume.html', {'resume': resume})

# @login_required
# def download_resume(request, resume_id):
#     resume = get_object_or_404(Resume, id=resume_id, user=request.user)

#     # Create a PDF response
#     buffer = BytesIO()
#     pdf = canvas.Canvas(buffer)

#     # Write resume details to the PDF
#     pdf.setTitle(f"Resume_{resume.id}")
#     pdf.setFont("Helvetica-Bold", 16)
#     pdf.drawString(100, 800, "Resume")

#     pdf.setFont("Helvetica", 12)
#     pdf.drawString(100, 770, f"Name: {resume.name}")
#     pdf.drawString(100, 750, f"Email: {resume.email}")
#     pdf.drawString(100, 730, f"Phone: {resume.phone}")
#     pdf.drawString(100, 710, f"Skills: {resume.skills}")
#     pdf.drawString(100, 690, f"Experience: {resume.experience}")
#     pdf.drawString(100, 670, f"Education: {resume.education}")

#     # Add more fields if necessary

#     pdf.save()
#     buffer.seek(0)

#     # Return the PDF as a response
#     response = HttpResponse(buffer, content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="resume_{resume.id}.pdf"'
#     return response











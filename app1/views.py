from django.shortcuts import render, HttpResponse
# For Flash Messages
from django.contrib import messages

import os
from docx2txt import docx2txt  # for DOCX files
from PyPDF2 import PdfReader  # for PDF files

# Create your views here.
def main(request):
    # messages.success(request, 'The post has been created successfully.')
    #return HttpResponse("Hello, World!")
    return render(request,'base.html')

# def upload_document(request):
#     if request.method == 'POST':
#         uploaded_document = request.FILES.get('document')

#         if uploaded_document:
#             # Save the document to a temporary location or process it directly
#             # For example, you can save it to the media folder
#             document_path = f'media/{uploaded_document.name}'
#             with open(document_path, 'wb+') as destination:
#                 for chunk in uploaded_document.chunks():
#                     destination.write(chunk)

#             # Extract text from the uploaded document
#             text = docx2txt.process(document_path)

#             # Pass the text to the template or do whatever you need with it
#             # return render(request, 'check.html', {'text': text})
#             return HttpResponse(text)

# def upload_document(request):
#     if request.method == 'POST':
#         uploaded_file = request.FILES['document']
#     # Determine file format and extract text accordingly
#         if uploaded_file.content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
#             # DOCX file
#             text = docx2txt.process(uploaded_file)
#         elif uploaded_file.content_type == 'application/pdf':
#             # PDF file using PyPDF2
#             reader = PdfReader(uploaded_file)
#             text = ''
#             for page in reader.pages:
#                 text += page.extract_text()
#         elif uploaded_file.content_type == 'text/plain':
#             # TXT file
#             with open(uploaded_file, 'r') as f:
#                 text = f.read()
#         else:
#             text = 'Unsupported file format'

#         return HttpResponse(text)

import os
from django.http import HttpResponse
from PyPDF2 import PdfReader
import docx2txt

def upload_document(request):
    try:
        if request.method == 'POST':
            uploaded_file = request.FILES['document']

            # Save the uploaded file to a temporary location
            temporary_file_path = 'media/temporary_file'
            with open(temporary_file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Determine file format and extract text accordingly
            if uploaded_file.content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                # DOCX file
                text = docx2txt.process(temporary_file_path)
            elif uploaded_file.content_type == 'application/pdf':
                # PDF file using PyPDF2
                reader = PdfReader(temporary_file_path)
                text = ''
                for page in reader.pages:
                    text += page.extract_text()
            elif uploaded_file.content_type == 'text/plain':
                # TXT file
                with open(temporary_file_path, 'r') as f:
                    text = f.read()
            else:
                text = 'Unsupported file format'

            # Remove the temporary file
            os.remove(temporary_file_path)

            return HttpResponse(text)

    except Exception as e:
        # Handle exceptions (e.g., file not found, extraction error)
        return HttpResponse(f'Error: {str(e)}')


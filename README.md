# DocSummarizationTool
 
# Automatic Text Summarization Web Application

This Django-based web application is designed to perform automatic text summarization on various document formats, including DOCX, PDF, and plain text files. The summarized text can be generated after uploading a document, and the application supports flash messages for user feedback.

## Features

- Supports DOCX, PDF, and plain text file formats
- Flash messages for user feedback
- Automatic text summarization using nltk and heapq libraries

# Getting Started

## Clone the repository:
git clone https://github.com/nassrkhan/Automatic-Text-Summarization-Web-Application.git


## Navigate to the project directory:
cd document-summarization

## Run the Django development server:
python manage.py runserver
Open your web browser and visit http://localhost:8000/ to access the application.

Upload a document on the main page to extract text and view the summary on the following page.

# File Structure
summarization/views.py: Contains Django views for document upload and text summarization.
media/: Temporary storage for uploaded files.
templates/: HTML templates for rendering pages.

# Acknowledgements
Django
nltk
docx2txt
PyPDF2

## Prerequisites

Make sure you have the following installed:

- Python 3.x
- Django
- nltk (Natural Language Toolkit)
- docx2txt
- PyPDF2

You can install the required Python packages using:

```bash
pip install django nltk docx2txt PyPDF2


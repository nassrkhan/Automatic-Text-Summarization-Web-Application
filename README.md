# DocSummarizationTool
 
# Automatic Text Summarization Web Application

This Django-based web application is designed to perform automatic text summarization on various document formats, including DOCX, PDF, and plain text files. The summarized text can be generated after uploading a document, and the application supports flash messages for user feedback.

## Features

- Supports DOCX, PDF, and plain text file formats
- Flash messages for user feedback
- Automatic text summarization using nltk and heapq libraries

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

from django.shortcuts import render, HttpResponse
# For Flash Messages
from django.contrib import messages

import os
import docx2txt  # for DOCX files
from PyPDF2 import PdfReader  # for PDF files

import re
import nltk
import heapq

# Create your views here.
def main(request):
    return render(request,'base.html')

global text
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
                messages.success(request, 'Unsupported file format !')

            # Remove the temporary file
            os.remove(temporary_file_path)

            messages.success(request, 'Text Extractted Successfully !')
            
            return render(request, 'showText.html', {'extracted_text': text})

    except Exception as e:
        # Handle exceptions (e.g., file not found, extraction error)
        messages.error(request, 'Incorrect File Format: {}'.format(str(e)))
    return render(request, 'showText.html')

def summarization(request):
    if request.method == 'POST':
        # Get the article text from the form data
        article_text = request.POST.get('extracted_text', '')

        # Preprocessing steps

        # Removing Square Brackets and Extra Spaces
        article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
        article_text = re.sub(r'\s+', ' ', article_text)
        # Removing special characters and digits
        formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
        formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
        sentence_list = nltk.sent_tokenize(article_text)
        stopwords = nltk.corpus.stopwords.words('english')

        word_frequencies = {}
        for word in nltk.word_tokenize(formatted_article_text):
            if word not in stopwords:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1
            maximum_frequncy = max(word_frequencies.values())
        for word in word_frequencies.keys():
            word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
            sentence_scores = {}
        for sent in sentence_list:
            for word in nltk.word_tokenize(sent.lower()):
                if word in word_frequencies.keys():
                    if len(sent.split(' ')) < 30:
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word]
                        else:
                            sentence_scores[sent] += word_frequencies[word]
        import heapq
        summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

        summary = ' '.join(summary_sentences)
        output_text = re.sub(r'\W', ' ', str(summary))

        messages.success(request, 'Summary Generated Successfully !')

        return render(request, 'showSumText.html', {'sum_text': summary})
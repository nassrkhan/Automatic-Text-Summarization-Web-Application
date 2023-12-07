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
    messages.success(request, 'The post has been created successfully.')
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
                text = 'Unsupported file format'

            # Remove the temporary file
            os.remove(temporary_file_path)
            
            return render(request, 'show.html', {'extracted_text': text})

    except Exception as e:
        # Handle exceptions (e.g., file not found, extraction error)
        return HttpResponse(f'Error: {str(e)}')

# def summarization(request):

#     if request.method == 'POST':
#         article_text = request.POST.get('extracted_text', '')

#         # article_text = extracted_text

#         # Removing Square Brackets and Extra Spaces
#         article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
#         article_text = re.sub(r'\s+', ' ', article_text)
#         # Remove non-word characters
#         article_text = re.sub(r'\W', ' ', article_text)
#         # Single Character Removal
#         article_text = re.sub(r'\s+[a-zA-Z]\s+', ' ', article_text)
#         article_text = re.sub(r'\^[a-zA-Z]\s+', ' ', article_text)
#         # Leading 'b' Removal
#         article_text = re.sub(r'^b\s+', '', article_text)
#         # Leading and Trailing Whitespaces Removal
#         article_text = re.sub(r'^\s', '', article_text)
#         article_text = re.sub(r'\s$', '', article_text)
#         # Multiple Spaces Removal
#         article_text = re.sub(r'\s+', ' ', article_text, flags=re.I)
#         # Removing special characters and digits
#         formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
#         formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
#         sentence_list = nltk.sent_tokenize(formatted_article_text)
#         stopwords = nltk.corpus.stopwords.words('english')

#         word_frequencies = {}
#         for word in nltk.word_tokenize(formatted_article_text):
#             if word not in stopwords:
#                 if word not in word_frequencies.keys():
#                     word_frequencies[word] = 1
#                 else:
#                     word_frequencies[word] += 1
#             maximum_frequncy = max(word_frequencies.values())
#         for word in word_frequencies.keys():
#             word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
#             sentence_scores = {}
#         for sent in sentence_list:
#             for word in nltk.word_tokenize(sent.lower()):
#                 if word in word_frequencies.keys():
#                     if len(sent.split(' ')) < 30:
#                         if sent not in sentence_scores.keys():
#                             sentence_scores[sent] = word_frequencies[word]
#                         else:
#                             sentence_scores[sent] += word_frequencies[word]
#         import heapq
#         summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

#         summary = ' '.join(summary_sentences)
        
#         return HttpResponse(summary)
        # return render(request, 'show.html', {'extracted_text': summary})

def summarization(request):
    if request.method == 'POST':
        # Get the article text from the form data
        ex_text = request.POST.get('extracted_text', '')

        # Preprocessing steps

        # Remove square brackets and extra spaces
        article_text = re.sub(r'\[[0-9]*\]', ' ', ex_text)
        article_text = re.sub(r'\s+', ' ', article_text)

        # Remove non-word characters
        article_text = re.sub(r'\W', ' ', article_text)

        # Single character removal
        article_text = re.sub(r'\s+[a-zA-Z]\s+', ' ', article_text)
        article_text = re.sub(r'\^[a-zA-Z]\s+', ' ', article_text)

        # Leading 'b' removal
        article_text = re.sub(r'^b\s+', '', article_text)

        # Leading and trailing whitespaces removal
        article_text = re.sub(r'^\s', '', article_text)
        article_text = re.sub(r'\s$', '', article_text)

        # Remove multiple spaces
        article_text = re.sub(r'\s+', ' ', article_text, flags=re.I)

        # Removing special characters and digits
        formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
        formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
        
        # Tokenize the sentences
        sentence_list = nltk.sent_tokenize(article_text)

        # Get English stopwords
        stopwords = nltk.corpus.stopwords.words('english')

        # Calculate word frequencies in the article
        word_frequencies = {}
        for word in nltk.word_tokenize(formatted_article_text.lower()):
            if word not in stopwords:
                if word not in word_frequencies:
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1

        # Normalize word frequencies
        maximum_frequency = max(word_frequencies.values())
        for word in word_frequencies:
            word_frequencies[word] = (word_frequencies[word] / maximum_frequency)

        # Calculate sentence scores based on word frequencies
        sentence_scores = {}
        for sent in sentence_list:
            for word in nltk.word_tokenize(sent.lower()):
                if word in word_frequencies:
                    if len(sent.split(' ')) < 30:
                        if sent not in sentence_scores:
                            sentence_scores[sent] = word_frequencies[word]
                        else:
                            sentence_scores[sent] += word_frequencies[word]

        # Get the top 7 sentences as the summary
        summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
        summary = ' '.join(summary_sentences)

        # print(summary)

        return HttpResponse(summary)
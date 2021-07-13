from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
import json
import PyPDF2
from elasticsearch import Elasticsearch
from fpdf import FPDF
import base64
from pydrive.auth import GoogleAuth
gauth = GoogleAuth()

from pydrive.drive import GoogleDrive
drive = GoogleDrive(gauth)

import io
import os

from tika import parser  
from .models import Content


def authentication(request):
    gauth.LocalWebserverAuth()
    return HttpResponse("Authentication Successfull")

elastic_client = Elasticsearch(hosts=["localhost"])

def download_file(request):
    file_list = drive.ListFile({'q': 'trashed=false'}).GetList()
    obj = Content.objects.all()
    l=[]
    if len(obj)!=0:
        for file in obj:
            if file.fileName not in l:
                l.append(file.fileName)

    for item in file_list:
        mimetypes = {
            'application/vnd.google-apps.document': 'application/pdf',
        }

        if item['mimeType'] in mimetypes:
            download_mimetype = mimetypes[item['mimeType']]
            fname='{}.pdf'.format(item['title'])
            item.GetContentFile(fname, mimetype=download_mimetype)
            parsed_pdf = parser.from_file(fname)
            data = parsed_pdf['content']

            if len(obj)==0:
                content_obj = Content.objects.create(fileName=item['title'], content=data,link=item['alternateLink'])
                content_obj.save()

            else:
                if item['title'] not in l:
                    content_obj=Content.objects.create(fileName=item['title'],content=data,link=item['alternateLink'])
                    content_obj.save()
    for file_name in l:
        file = file_name+".pdf"
        read_pdf = PyPDF2.PdfFileReader(file, strict=False)

        pdf_meta = read_pdf.getDocumentInfo()

        num = read_pdf.getNumPages()

        all_pages = {}

        all_pages["meta"] = {}

        for meta, value in pdf_meta.items():
            all_pages["meta"][meta] = value

        for page in range(num):
            data = read_pdf.getPage(page)

            page_text = data.extractText()

            all_pages[page] = page_text

        json_data = json.dumps(all_pages)

        bytes_string = bytes(json_data, 'utf-8')

        encoded_pdf = base64.b64encode(bytes_string)
        encoded_pdf = str(encoded_pdf)

        body_doc = {"data": encoded_pdf}

        result = elastic_client.index(index=("{}".format(file[:-4]).lower().replace(" ","")), doc_type="_doc", id="42", body=body_doc)

        result = elastic_client.get(index=("{}".format(file[:-4]).lower().replace(" ","")), doc_type='_doc', id=42)

        result_data = result["_source"]["data"]

        decoded_pdf = base64.b64decode(result_data[2:-1]).decode("utf-8")

        json_dict = json.loads(decoded_pdf)

    data = {'status_code': status.HTTP_200_OK,
            'status_message': "Success"
            }
    qs_json = json.dumps(data)
    return HttpResponse(qs_json, content_type='application/json')



def searchcontent(request):
    param=request.GET['q']
    l=[]
    con_obj = Content.objects.all()
    for con in con_obj:
        if param in con.content:
            if con.link not in l:
                l.append(con.link)

    data = {'status_code': status.HTTP_200_OK,
            'status_message': "Success",
            'list':l
            }
    qs_json = json.dumps(data)
    return HttpResponse(qs_json, content_type='application/json')
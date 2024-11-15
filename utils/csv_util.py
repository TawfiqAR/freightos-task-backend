from fastapi import FastAPI, File, UploadFile, APIRouter
import csv
import codecs

def convert_to_json(file: UploadFile = File(...)):
    csv_reader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))
    data = {}
    line_number = 1
    for rows in csv_reader:
        key = line_number
        line_number+=1
        data[key] = rows
    file.file.close()
    return data
# For http-operasjoner
import asyncio
import io
import json

import js
import pandas as pd
from analyse import analyse
from js import FileReader, document
from pyodide import create_proxy
from pyodide.http import open_url
from request import request  # import our request function.
from saft2dataframe import saft2dataframe


# For demo av http-forespørsler ved hjelp av request.py
# kjøres med asyncio.ensure_future(http_request_demo())
async def http_request_demo():
    baseurl = "https://jsonplaceholder.typicode.com"

    # GET
    headers = {"Content-type": "application/json"}
    response = await request(f"{baseurl}/posts/2", method="GET", headers=headers)
    print(f"GET request=> status:{response.status}, json:{await response.json()}")

    # POST
    body = json.dumps({"title": "test_title", "body": "test body", "userId": 1})
    new_post = await request(f"{baseurl}/posts", body=body, method="POST", headers=headers)
    print(f"POST request=> status:{new_post.status}, json:{await new_post.json()}")

    # PUT
    body = json.dumps({"id": 1, "title": "test_title", "body": "test body", "userId": 2})
    new_post = await request(f"{baseurl}/posts/1", body=body, method="PUT", headers=headers)
    print(f"PUT request=> status:{new_post.status}, json:{await new_post.json()}")

    # DELETE
    new_post = await request(f"{baseurl}/posts/1", method="DELETE", headers=headers)
    print(f"DELETE request=> status:{new_post.status}, json:{await new_post.json()}")


  
# Koden for å lese fil er hentet fra her:
# https://github.com/amrrs/pyscript-file-uploader/blob/main/index.html

saft_innhold = ""  # global variabel, teksten fra saft-fila
saft = pd.DataFrame()  # global variabel

def hent_saft_innhold() -> io.StringIO:
    if saft_innhold == "":
        print('Du må først velge en lokal fil')
        return None
    else:
        print(f'Her er saft_innhold: {saft_innhold[:100]}')
        return io.StringIO(saft_innhold)

def read_complete(event) -> pd.DataFrame:
# event is ProgressEvent

    content = document.getElementById("content")
    global saft_innhold, saft
    saft_innhold = event.target.result
    print(f'Har oppdatert saft_innhold: {saft_innhold[:100]}')

    # kjør denne cellen (Shift-Enter) for hente dataene
    # fra filen du har valgt
    saft = saft2dataframe(hent_saft_innhold())
    print(f'har oppdatert saft dataframe')


async def process_file(x):
    fileList = document.getElementById('myfile').files

    for f in fileList:
        # reader is a pyodide.JsProxy
        reader = FileReader.new()

        # Create a Python proxy for the callback function
        onload_event = create_proxy(read_complete)

        #console.log("done")

        reader.onload = onload_event

        reader.readAsText(f)

        return  # lurer litt på hvorfor det er return inne i for-løkken ... kanskje en typo av meg?


def oppsett_for_lesing_av_lokal_fil():
    # Create a Python proxy for the callback function
    file_event = create_proxy(process_file)

    # Set the listener to the callback
    e = document.getElementById("myfile")
    e.addEventListener("change", file_event, False)


oppsett_for_lesing_av_lokal_fil()
   

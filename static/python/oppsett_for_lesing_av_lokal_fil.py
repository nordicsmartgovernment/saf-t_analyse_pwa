# Koden for å lese fil er hentet fra her:
# https://github.com/amrrs/pyscript-file-uploader/blob/main/index.html
import asyncio
import js
from js import document, FileReader
from pyodide import create_proxy
import io
from saft2dataframe import saft2dataframe
import pandas as pd

import s

saft_innhold = ""  # global variabel, teksten fra saft-fila
# saft = pd.DataFrame()  # global variabel


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
    global saft_innhold
    saft_innhold = event.target.result
    print(f'Har oppdatert saft_innhold: {saft_innhold[:100]}')

    # kjør denne cellen (Shift-Enter) for hente dataene
    # fra filen du har valgt
    s.aft = saft2dataframe(hent_saft_innhold())
    print(f'har oppdatert s.aft dataframe')


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


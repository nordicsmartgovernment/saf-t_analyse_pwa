# For http-operasjoner
import asyncio
import json
from request import request  # import our request function.


import pandas as pd
from pyodide.http import open_url

from saft2dataframe import saft2dataframe
from analyse import analyse
from oppsett_for_lesing_av_lokal_fil import oppsett_for_lesing_av_lokal_fil, hent_saft_innhold  # sistnevnte brukes ikke her, men i index.html

import s

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


# import os
# print('Current Working Directory:')
# print(os.getcwd())

# print('Root directory contents:')
# files = os.listdir('/')
# for file in files:
#         print(file)
  


oppsett_for_lesing_av_lokal_fil()
   

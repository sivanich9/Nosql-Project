from fastapi import FastAPI, status, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
import urllib.request 

url = "https://pkwxbrxicmbncxgcblbv.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBrd3hicnhpY21ibmN4Z2NibGJ2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODQxNjEzMDksImV4cCI6MTk5OTczNzMwOX0.AlBih_pbLn3jhcPqp0o-a0CP-80nO02PD7lM4UtiVuA";

supabase = create_client(url, key)


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class Ingestion(BaseModel):
    xmlfilePath: str
    datafilePath: str 


@app.get("/")
async def root():
    return {"message": "hello world"}



@app.post("/ingest")
async def ingest_files(ingestion: Ingestion):
    print(ingestion)
    xmlpath = supabase.storage.from_("pig_storage").get_public_url(ingestion.xmlfilePath)
    datapath = supabase.storage.from_("pig_storage").get_public_url(ingestion.datafilePath)
    print(xmlpath, datapath)

    with open("./pig_ingest.xml", 'wb+') as f:
        res = supabase.storage.from_("pig_storage").download(ingestion.xmlfilePath)
        f.write(res)

    
    with open("./datafile.tsv", 'wb+') as f:
        res = supabase.storage.from_("pig_storage").download(ingestion.datafilePath)
        f.write(res)
            

    return {"ingestion": "ok"}

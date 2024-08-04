from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PdfProcesses import PdfProcesses
from web_scrape import web_scrape
import constants
from selenium.common.exceptions import TimeoutException
from pathlib import Path

app = FastAPI()

@app.post("/doc-verify")
async def doc_verify(file: UploadFile = File(...)):

    Path('temp').mkdir(parents=True, exist_ok=True)

    file_path = f'temp/{file.filename}'
    new_file_path = ''
    
    try:

        PdfProcesses.save_pdf(file_path, file)

        data_ = PdfProcesses.read_pdf(file_path)

        constants.CURRENT_USER_ID_NUMBER = data_['id_number']

        web_scrape(data_['doc_code'], data_['id_number'])

        new_file_path = f'temp/{data_['doc_code']}.pdf'

        data = PdfProcesses.read_pdf(new_file_path)

        PdfProcesses.move_pdf(new_file_path, f'{data['id_number']}.pdf')

        return JSONResponse(content={"data": data}, status_code=200)
    except TimeoutException as e:
        if new_file_path != '': PdfProcesses.delete_pdf(new_file_path)
        return JSONResponse(content={"error": str(e.msg)}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        PdfProcesses.delete_pdf(file_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
from fastapi import FastAPI, File, UploadFile, Form
import pandas as pd
import zipfile
import io

app = FastAPI()

@app.post("/api/")
async def process_question(question: str = Form(...), file: UploadFile = File(None)):
    if file:
        content = await file.read()
        with zipfile.ZipFile(io.BytesIO(content)) as z:
            z.extractall("./extracted")
        
        csv_file = [f for f in z.namelist() if f.endswith('.csv')][0]
        df = pd.read_csv(f"./extracted/{csv_file}")
        
        # Assuming the question asks for the 'answer' column's value
        if 'answer' in df.columns:
            answer_value = df['answer'].iloc[0]
            return {"answer": str(answer_value)}
        else:
            return {"answer": "The 'answer' column was not found in the CSV file."}
    else:
        # Placeholder logic for handling questions without file upload
        return {"answer": "This is a placeholder response. Implement your LLM logic here."}

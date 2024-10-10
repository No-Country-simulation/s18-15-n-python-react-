from fastapi import FastAPI


app =  FastAPI()


@app.get('/')
async def getData(): 
    return {"message": "Hello, World32!"}


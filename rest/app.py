from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def sayHello():
	return(dict(
		hello='world'
	))
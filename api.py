from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from utils import random_image, random_string
from pynng import Req0
import uvicorn

app = Starlette(debug=True)
app.mount('/static', app=StaticFiles(directory='static'), name='static')

s = Req0(listen='tcp://127.0.0.1:54321')

templates = Jinja2Templates(directory='static')

@app.route('/')
async def homepage(request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.route('/api/response')
async def response(request):
    await s.asend(b'message')
    message = await s.arecv()
    return JSONResponse({'hello': message.decode()})


@app.route('/api/data')
async def data(request):
    return JSONResponse({'string': random_string(),
                         'image': random_image().decode()})
    

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8800)

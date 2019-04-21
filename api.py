from starlette.applications import Starlette
from starlette.responses import UJSONResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.schemas import SchemaGenerator
from utils import random_image, random_string
from datetime import datetime
from pynng import Req0
import uvicorn


schemas = SchemaGenerator(
    {"openapi": "3.0.0", "info": {"title": "Example API",
                                  "version": "1.0"}}
    )
app = Starlette(debug=True)
app.mount('/static', app=StaticFiles(directory='static'), name='static')

s = Req0(listen='tcp://127.0.0.1:54321')

templates = Jinja2Templates(directory='static')

@app.route('/')
async def homepage(request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.route("/schema", methods=["GET"], include_in_schema=False)
def openapi_schema(request):
    return schemas.OpenAPIResponse(request=request)


@app.route('/api/data', methods=['GET'])
async def data(request):
    """
    responses:
      200:
        description: Data for the application
        examples:
            {"string": "blahblah",
             "key": "a237b223",
             "image": "image/png;base64,ivfhei2..."}
    """
    return UJSONResponse(
        {'string': random_string(),
         'key': random_string(),
         'image': f'data:image/png;base64,{random_image().decode()}'})
    

@app.route('/api/response', methods=['POST'])
async def response(request):
    await s.asend(await request.body())
    message = await s.arecv()
    return UJSONResponse({'status': 'ok'})


def main(host='0.0.0.0', port=8800):
    uvicorn.run(app, host=host, port=port)

if __name__ == '__main__':
    main()

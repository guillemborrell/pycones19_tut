from starlette.applications import Starlette
from starlette.responses import JSONResponse
from pynng import Req0
import uvicorn

app = Starlette(debug=True)

s = Req0(listen='tcp://127.0.0.1:54321')

@app.route('/')
async def homepage(request):
    await s.asend(b'message')
    message = await s.arecv()
    return JSONResponse({'hello': message.decode()})


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8800)

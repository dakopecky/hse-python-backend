import json
import math
from urllib.parse import parse_qs


async def app(scope, receive, send):
    if scope['type'] == 'http':
        method = scope['method']
        path = scope['path']

        if method == 'GET' and path == '/factorial':
            await handle_factorial(scope, receive, send)
        elif method == 'GET' and path.startswith('/fibonacci/'):
            await handle_fibonacci(scope, receive, send)
        elif method == 'GET' and path == '/mean':
            await handle_mean(scope, receive, send)
        else:
            await send_404(send)


async def handle_factorial(scope, receive, send):
    query_string = scope['query_string'].decode()
    query_params = parse_qs(query_string)

    if 'n' not in query_params:
        await send_422(send, "Missing parameter 'n'")
        return

    try:
        n = int(query_params['n'][0])
        if n < 0:
            await send_400(send, "Parameter 'n' must be a non-negative integer.")
            return
        result = math.factorial(n)
        await send_json(send, {"result": result})
    except (ValueError, IndexError):
        await send_422(send, "Invalid parameter 'n'. It must be an integer.")
    except Exception as e:
        await send_500(send, str(e))


async def handle_fibonacci(scope, receive, send):
    path = scope['path']
    try:
        n = int(path.split('/')[-1])
        if n < 0:
            await send_400(send, "Parameter 'n' must be a non-negative integer.")
            return

        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b

        await send_json(send, {"result": a})
    except ValueError:
        await send_422(send, "Invalid parameter 'n'. It must be an integer.")
    except Exception as e:
        await send_500(send, str(e))


async def handle_mean(scope, receive, send):
    body = await receive_body(receive)

    try:
        data = json.loads(body)
        if not isinstance(data, list) or len(data) == 0:
            await send_400(send, "Body must be a non-empty array of floats.")
            return
        if not all(isinstance(i, (int, float)) for i in data):
            await send_422(send, "All elements in the array must be floats or integers.")
            return

        result = sum(data) / len(data)
        await send_json(send, {"result": result})
    except json.JSONDecodeError:
        await send_422(send, "Request body must be a valid JSON.")
    except Exception as e:
        await send_500(send, str(e))


async def send_json(send, data):
    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [(b'content-type', b'application/json')]
    })
    await send({
        'type': 'http.response.body',
        'body': json.dumps(data).encode('utf-8')
    })


async def send_400(send, message):
    await send({
        'type': 'http.response.start',
        'status': 400,
        'headers': [(b'content-type', b'application/json')]
    })
    await send({
        'type': 'http.response.body',
        'body': json.dumps({"error": message}).encode('utf-8')
    })


async def send_404(send):
    await send({
        'type': 'http.response.start',
        'status': 404,
        'headers': [(b'content-type', b'application/json')]
    })
    await send({
        'type': 'http.response.body',
        'body': json.dumps({"error": "Not Found"}).encode('utf-8')
    })


async def send_422(send, message):
    await send({
        'type': 'http.response.start',
        'status': 422,
        'headers': [(b'content-type', b'application/json')]
    })
    await send({
        'type': 'http.response.body',
        'body': json.dumps({"error": message}).encode('utf-8')
    })


async def send_500(send, message):
    await send({
        'type': 'http.response.start',
        'status': 500,
        'headers': [(b'content-type', b'application/json')]
    })
    await send({
        'type': 'http.response.body',
        'body': json.dumps({"error": message}).encode('utf-8')
    })


async def receive_body(receive):
    body = b''
    while True:
        message = await receive()
        if message['type'] == 'http.request':
            body += message.get('body', b'')
            if not message.get('more_body', False):
                break
    return body

import gzip
import json

from chalice import Chalice, Response

app = Chalice(app_name='cors-gzip-repro')
app.api.binary_types.append('application/json')  # This breaks OPTIONS


@app.route('/', methods=['GET'], cors=True)
def index():
    data = {'hello': 'world'}
    serialized = json.dumps(data)
    blob = gzip.compress(serialized.encode('utf-8'))

    return Response(
        body=blob,
        status_code=200,
        headers={
            'Content-Type': 'application/json',
            'Content-Encoding': 'gzip'
        }
    )


@app.route('/echo', methods=['POST'], cors=True)
def post_echo():
    data = app.current_request.json_body
    serialized = json.dumps(data)
    blob = gzip.compress(serialized.encode('utf-8'))

    return Response(
        body=blob,
        status_code=200,
        headers={
            'Content-Type': 'application/json',
            'Content-Encoding': 'gzip'
        }
    )

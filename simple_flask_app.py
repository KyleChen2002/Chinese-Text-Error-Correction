from flask import request, Flask

app = Flask(__name__)


@app.before_request
def before_request():
    # app.logger.info(f"before_request. {request.url}")
    print(f'before_request. request.path: {request.path}')
    print(f'before_request. request.body: {request.get_data()}')
    return return_ok(), 200, [("Content-Type", "application/json")]


def return_ok():
    return '{"OUT": {"RtnCode": "0000"}}'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)

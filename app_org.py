from flask import request, abort, redirect, render_template, session, make_response, g, flash
from markupsafe import escape
import flaskr
import logging
from logging import FileHandler
import re
from pycorrector.macbert.macbert_corrector import MacBertCorrector

def set_log(app):
    print('set_log start')
    gunicorn_logger = logging.getLogger('gunicorn.error')
    print(f'gunicorn_logger.handlers: {gunicorn_logger.handlers}')
    print(f'gunicorn_logger.level: {gunicorn_logger.level}')

    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    print(f'app.logger.handlers: {app.logger.handlers}')
    print(f'app.logger.level: {app.logger.level}')
    print(f'app.name: {app.name}')

    print('set_log end')


def set_log2(app):
    app.debug = True
    handler = logging.FileHandler('flask.log')
    app.logger.addHandler(handler)
    print('set_log2 end')
    app.logger.info('123123123')


app = flaskr.create_app()
#set_log(app)
set_log2(app)

# before_request 登录校验白名单
white_list = ['/login.html', '/demo.html', '/static']

m = MacBertCorrector()


@app.before_request
def before_request():
    # app.logger.info(f"before_request. {request.url}")
    #print('print 1 before_request')
    #app.logger.debug('debug before_request')
    #app.logger.info('debug before_request')
    #app.logger.error('error before_request')

    # if request.path in white_list:
    #     return None
    for white in white_list:
        if request.path.startswith(white):
            return None


@app.route("/")
@app.route("/demo.html", methods=['GET'])
def login_page():
    return render_template('demo.html')

@app.route("/do_check", methods=['POST'])
def do_check():
    input_text = request.form['input_text']
    print(f"1. input_text: {input_text}")
    app.logger.info(f"input_text: {input_text}")

    # app.logger.info(f"changepwd. 1 user: {user} old_password: {escape(old_password)} new_password: {escape(new_password)} new2_password: {escape(new2_password)}!")

    check_result_list = correct(input_text)
    check_result = 'check_result'
    check_result = "\n".join(check_result_list)

    # check pwd
    if True:
        if check_result == "":
            check_result = "==> 未检测到错误 ==<"
        flash(check_result)
        # abort(400)
        return render_template('demo.html', last_input=input_text)

    print(f"2. check_result: {check_result}")
    app.logger.info(f"check_result: {check_result}")

    return res


def correct(input_text):
    global m
    check_result_list = []
    if not input_text:
        return check_result_list

    app.logger.info(f"input_text: {input_text}")
    #error_sentences = input_text.split("\n")
    error_sentences = re.split(r"[\n。！？，]",input_text)
    
    for line in error_sentences:
        print("error_sentences:{}\n".format(line))
        if line is None or line == "":
            print('empty line. skip')
            continue
        correct_sent, err = m.macbert_correct(line)
        if len(err) == 0:
            continue
        print("\n\nquery:{}\n   => {}\n  err:{}".format(line, correct_sent, err))
        check_result_list.append("=> {}\n  err:{}".format(correct_sent, err))

    return check_result_list


def correct2():
    m = MacBertCorrector()
    input_file = 'input.txt'
    check_result_list = []
    with open(input_file, 'r', encoding='utf-8') as f:
        error_sentences = f.readlines()

        for line in error_sentences:
            print("error_sentences:{}\n".format(line))
            correct_sent, err = m.macbert_correct(line)
            if len(err) == 0:
                continue
            print("\n\nquery:{}\n   => {}\n  err:{}".format(line, correct_sent, err))
            check_result_list.append("query:{}\n   => {}\n  err:{}".format(line, correct_sent, err))
    return check_result_list


# if __name__ == '__main__':
#    gunicorn_logger = logging.getLogger('gunicorn.error')
#    app.logger.handlers = gunicorn_logger.handlers
#    #app.logger.setLevel(gunicorn_logger.level)
#    app.logger.setLevel(logging.DEBUG)
#    app.run(debug=False)


if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=5001)

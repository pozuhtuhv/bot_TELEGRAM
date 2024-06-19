# 코인 현재 가격정보

import requests

def info(context, SERVER_URL, UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY):
    # 명령어 뒤에 입력된 인수를 받아옴.
    args = context.args

    headers = {"accept": "application/json"}

    response = requests.get(SERVER_URL+"?markets="+args, headers=headers)

    print(response.json())

    if args:
        msg = f"info: {' '.join(args)}"
    else:
        msg = "info가 입력되지 않았습니다. '/info <내용>' 형식으로 입력해주세요."






    return msg
def info(context):
    # 명령어 뒤에 입력된 인수를 받아옴.
    args = context.args
    if args:
        msg = f"info: {' '.join(args)}"
    else:
        msg = "info가 입력되지 않았습니다. '/info <내용>' 형식으로 입력해주세요."
    return msg
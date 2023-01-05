import base64


def encode_command_to_markdown(name: str, command: str, arg: str = None) -> str:
    template = open("controller_request_template.md", "r")
    template_data = template.read().replace("@NAME", name).replace("@COMMAND", command)
    if arg is not None:
        template_data = template_data.replace("@ARG", arg)
    template.close()
    return template_data


def encode_data_to_markdown(data: str) -> str:
    template = open("bot_response_template.md", "r")
    template_data = template.read().replace("@DATA", data)
    template.close()
    return template_data


def decode_data_from_markdown(data: str) -> str:
    return data.replace("Hello World!\n", "").replace("<!---", "").replace("-->", "")


def encode_data_to_base64(content) -> str:
    return base64.b64encode(content).decode("ascii")


def decode_data_from_base64(data_string: str) -> bytes:
    return base64.b64decode(data_string)

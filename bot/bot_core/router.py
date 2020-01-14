import re


def prepare_pattern(pattern):
    param_regex = re.compile("\(\?P<(\w+)>([^)(]+)\)")
    matches = param_regex.findall(pattern)

    raw_pattern = str(pattern)

    params = []
    values = {}
    for param, value in matches:
        params.append(param)
        values[param] = value

    for param in params:
        raw_pattern = raw_pattern.replace("(?P<%s>%s)" % (param, values[param]), "(%s)" % values[param])

    return raw_pattern, params


def get_kwargs(text_command, raw_pattern, params_list):
    regex = re.compile(raw_pattern)
    match = regex.match(text_command)

    values = {}

    for i in range(len(match.groups())):
        values[params_list[i]] = match.group(i+1)

    return values


def process_text_message(bot, update, text_patterns):
    text_command = update.message.text
    for pattern, command in text_patterns:
        raw_pattern, params_list = prepare_pattern(pattern)
        regex = re.compile(raw_pattern)
        if regex.fullmatch(text_command):
            kwargs = get_kwargs(text_command, raw_pattern, params_list)
            return command(bot, update, **kwargs)
    return False

def write_file(content, path, mode="wb"):
    with open(path, mode) as f:
        f.write(content)
    return path


def read_file(path, mode="r"):
    with open(path, mode) as f:
        content = f.read()
    return content

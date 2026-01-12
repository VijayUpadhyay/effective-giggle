def write_to_file(filename, content):
    with open(filename, "rw+") as f:
        f.write(content)
        f.close()


def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
        return None

    wrapper.has_run = False
    return wrapper

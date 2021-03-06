import errno
import os
try:
    from shlex import quote as shell_quote
except ImportError:
    from pipes import quote as shell_quote


def shell_quote_cmd(cmdlist):
    return ' '.join(map(shell_quote, cmdlist))


def format_cmdline(args, maxwidth=80):
    '''Format args into a shell-quoted command line.

    The result will be wrapped to maxwidth characters where possible,
    not breaking a single long argument.
    '''

    # Leave room for the space and backslash at the end of each line
    maxwidth -= 2

    def lines():
        line = ''
        for a in (shell_quote(a) for a in args):
            # If adding this argument will make the line too long,
            # yield the current line, and start a new one.
            if len(line) + len(a) + 1 > maxwidth:
                yield line
                line = ''

            # Append this argument to the current line, separating
            # it by a space from the existing arguments.
            if line:
                line += ' ' + a
            else:
                line = a

        yield line

    return ' \\\n'.join(lines())


def mkdir_p(path):
    # http://stackoverflow.com/a/600612/119527
    try:
        os.makedirs(path)
    except OSError as exc:
        if not (exc.errno == errno.EEXIST and os.path.isdir(path)):
            raise


def parse_env_var(s):
    """Parse an environment variable string

    Returns a key-value tuple

    Apply the same logic as `docker run -e`:
    "If the operator names an environment variable without specifying a value,
    then the current value of the named variable is propagated into the
    container's environment
    """
    parts = s.split('=', 1)
    if len(parts) == 2:
        k, v = parts
        return (k, v)

    k = parts[0]
    return (k, os.getenv(k, ''))

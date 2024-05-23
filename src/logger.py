
def log(status, msg):
    """
    Log a message prefixed by a status tag

    Parameters
    ----------
    status: string
        prefix status tag
    msg: any
        the print contents
    """

    print(f"[{status}] {msg}")


def info(msg):
    """
    Log a message prefixed by the INFO status tag

    Parameters
    ----------
    msg: any
        the print contents
    """

    log("INFO", msg)


def warn(msg):
    """
    Log a message prefixed by the WARN status tag

    Parameters
    ----------
    msg: any
        the print contents
    """

    log("WARN", msg)


def erro(msg):
    """
    Log a message prefixed by the ERRO status tag

    Parameters
    ----------
    msg: any
        the print contents
    """

    log("ERRO", msg)


def succ(msg):
    """
    Log a message prefixed by the SUCC status tag

    Parameters
    ----------
    msg: any
        the print contents
    """

    log("SUCC", msg)


def fail(msg):
    """
    Log a message prefixed by the FAIL status tag

    Parameters
    ----------
    msg: any
        the print contents
    """

    log("FAIL", msg)


def debu(msg):
    """
    Log a message prefixed by the DEBU status tag

    Parameters
    ----------
    msg: any
        the print contents
    """

    log("DEBU", msg)


def LOG(status, msg, hint = ""):
    """
    Log a message prefixed by a status tag

    Parameters
    ----------
    status: string
        prefix status tag
    msg: any
        the print contents
    """

    print(f"[{status}] {msg}", end="")
    if hint != "":
        print(f". Hint: {hint}")
    else:
        print("")


def INFO(msg):
    """
    Log a message prefixed by the INFO status tag

    Parameters
    ----------
    msg: any
        the print contents
    """

    LOG("INFO", msg)


def WARN(msg, hint = ""):
    """
    Log a message prefixed by the WARN status tag

    Parameters
    ----------
    msg: any
        the print contents
    """

    LOG("WARN", msg, hint)


def ERRO(msg, hint = ""):
    """
    Log a message prefixed by the ERRO status tag

    Parameters
    ----------
    msg: any
        the print contents
    """

    LOG("ERRO", msg, hint)


def SUCC(msg):
    """
    Log a message prefixed by the SUCC status tag

    Parameters
    ----------
    msg: any
        the print contents
    """

    LOG("SUCC", msg)


def FAIL(msg, hint = ""):
    """
    Log a message prefixed by the FAIL status tag

    Parameters
    ----------
    msg: any
        the print contents
    """

    LOG("FAIL", msg, hint)


def DEBU(msg):
    """
    Log a message prefixed by the DEBU status tag

    Parameters
    ----------
    msg: any
        the print contents
    """

    LOG("DEBU", msg)

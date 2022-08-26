from typing import Callable, Union
import requests
from contextlib import contextmanager

@contextmanager
def httpRequest(session, url, method, payload: dict = None, **params):
    """
    Generate a context to automatically send http request, allowing user to focus on response handling.

    Parameters
    ----------
    session : requests.Session
        Provide a session to be used.
    url : str
        Full url address with scheme 'http://' or 'https://'.
    method : str
        Only 'get' or 'post' is supported.
    payload : dict, optional
        This parameter is a lazy replacement for "params" and "data" (correspond to GET and POST respectively).
    **params :
        Additional arguments passed to package ``request``, such as headers and cookies.

    Returns
    -------
    requests.Response

    Examples
    --------
    >>> s = requests.Session()
    >>> with httpRequest(s, 'https://www.bilibili.com', 'get',
    ...                  payload={'key': 'data'},
    ...                  headers={},
    ...                  cookies={}) as resp:
    ...     # Handle the response object
    ...     print(resp.ok)
    True
    """
    if params is None:
        params = {}

    # Set default headers
    headers = params.setdefault('headers', {})
    UA = {
        'android':  'Mozilla/5.0 (Linux; Android 10; NOH-AN00 Build/HUAWEINOH-AN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3263 MMWEBSDK/20211202 Mobile Safari/537.36 MMWEBID/9462 MicroMessenger/8.0.18.2060(0x28001257) Process/toolsmp WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64',
        'pc': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }
    headers.setdefault('User-Agent',
                       UA['pc']
                       )

    if method not in ['get', 'post']:
        raise NotImplementedError('http method', method, 'is not supported!')

    if payload:
        # replace key 'payload' with the correct key
        payload_key = 'params' if method == 'get' else 'data'
        params[payload_key] = payload

    # send the request
    yield session.request(method, url, **params)


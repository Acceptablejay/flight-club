# read the comment below to confirm if you need this file

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
from urllib3.util.retry import Retry
import ssl


class TLS12Adapter(HTTPAdapter):
    """
    Transport adapter that enforces TLS 1.2
    """

    def init_poolmanager(self, *args, **kwargs):
        # Create a custom SSL context
        context = create_urllib3_context()
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.maximum_version = ssl.TLSVersion.TLSv1_2
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        context = create_urllib3_context()
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.maximum_version = ssl.TLSVersion.TLSv1_2
        kwargs['ssl_context'] = context
        return super().proxy_manager_for(*args, **kwargs)


def get_tls12_session():
    """
    Returns a requests.Session() object that:
      - Forces TLS 1.2
      - Handles retries for transient errors
    """
    session = requests.Session()

    # Mount TLS 1.2 adapter for HTTPS
    session.mount("https://", TLS12Adapter())

    # Optional: add retries
    retries = Retry(
        total=5,
        backoff_factor=0.5,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "PUT", "POST", "DELETE", "OPTIONS", "TRACE"]
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)

    return session


'''
#section 1
any error similar to...
C:/Users\HomePC\Downloads\PythonProject3\flight-club\.venv\Scripts\python.exe C:/Users\HomePC\Downloads\PythonProject3\flight-club\main.py 
Traceback (most recent call last):
  File "C:/Users\HomePC\Downloads\PythonProject3\flight-club\.venv\Lib\site-packages\/rllib3\connectionpool.py", line 464, in _make_request
    self._validate_conn(conn)
  File "C:/Users\HomePC\Downloads\PythonProject3\flight-club\.venv\Lib\site-packages\/rllib3\connectionpool.py", line 1093, in _validate_conn
    conn.connect()
  File "C:/Users\HomePC\Downloads\PythonProject3\flight-club\.venv\Lib\site-packages\/rllib3\connection.py", line 796, in connect
    sock_and_verified = _ssl_wrap_socket_and_match_hostname(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:/Users\HomePC\Downloads\PythonProject3\flight-club\.venv\Lib\site-packages\/rllib3\connection.py", line 975, in _ssl_wrap_socket_and_match_hostname
    ssl_sock = ssl_wrap_socket(
               ^^^^^^^^^^^^^^^^
  File "C:/Users\HomePC\Downloads\PythonProject3\flight-club\.venv\Lib\site-packages\/rllib3/util\ssl_.py", line 483, in ssl_wrap_socket
    ssl_sock = _ssl_wrap_socket_impl(sock, context, tls_in_tls, server_hostname)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:/Users\HomePC\Downloads\PythonProject3\flight-club\.venv\Lib\site-packages\/rllib3/util\ssl_.py", line 527, in _ssl_wrap_socket_impl
    return ssl_context.wrap_socket(sock, server_hostname=server_hostname)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:/Users\HomePC\AppData\Local\Programs\Python\Python311\Lib\ssl.py", line 517, in wrap_socket
    return self.sslsocket_class._create(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:/Users\HomePC\AppData\Local\Programs\Python\Python311\Lib\ssl.py", line 1104, in _create
    self.do_handshake()
  File "C:/Users\HomePC\AppData\Local\Programs\Python\Python311\Lib\ssl.py", line 1382, in do_handshake
    self._sslobj.do_handshake()
ssl.SSLEOFError: [SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1006)

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:/Users\HomePC\Downloads\PythonProject3\flight-club\.venv\Lib\site-packages/urllib3\connectionpool.py", line 787, in urlopen
    response = self._make_request(
               ^^^^^^^^^^^^^^^^^^^
  File "C:/Users\HomePC\Downloads\PythonProject3\flight-club\.venv\Lib\site-packages/urllib3\connectionpool.py", line 488, in _make_request
    raise new_e
urllib3.exceptions.SSLError: [SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1006)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "C:/Users\HomePC\Downloads\PythonProject3\flight-club\.venv\Lib\site-packages\requests\adapters.py", line 644, in send
    resp = conn.urlopen(
           ^^^^^^^^^^^^^
  File "C:/Users\HomePC\Downloads\PythonProject3\flight-club\.venv\Lib\site-packages/urllib3\connectionpool.py", line 841, in urlopen
    retries = retries.increment(
              ^^^^^^^^^^^^^^^^^^
  File "C:/Users\HomePC\Downloads\PythonProject3\flight-club\.venv\Lib\site-packages/urllib3/util\retry.py", line 535, in increment
    raise MaxRetryError(_pool, url, reason) from reason  # type: ignore[arg-type]
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='api.sheety.co', port=443): Max retries exceeded with url: /b3890d6367f62b8d2568e931b76eb133/flightDeals/sheet1 (Caused by SSLError(SSLEOFError(8, '[SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1006)')))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:Users\HomePC\Downloads\PythonProject3/flight-club\main.py", line 11, in <module>
    sheet_data = data_manager.get_destination_data()
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:Users\HomePC\Downloads\PythonProject3/flight-club\data_manager.py", line 22, in get_destination_data
    response = requests.get(url=SHEETY_PRICES_ENDPOINT,headers=headers, timeout=30, verify=False)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:Users\HomePC\Downloads\PythonProject3/flight-club\.venv\Lib\site-packages/requests/api.py", line 73, in get
    return request("get", url, params=params, **kwargs/
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^/
  File "C:Users\HomePC\Downloads\PythonProject3/flight-club\.venv\Lib\site-packages/requests/api.py", line 59, in request
    return session.request(method=method, url=url, **kwargs/
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^/
  File "C:Users\HomePC\Downloads\PythonProject3/flight-club\.venv\Lib\site-packages/requests/sessions.py", line 589, in request
    resp = self.send(prep, **send_kwargs/
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^/
  File "C:Users\HomePC\Downloads\PythonProject3/flight-club\.venv\Lib\site-packages/requests/sessions.py", line 703, in send
    r = adapter.send(request, **kwargs/
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^/
  File "C:Users\HomePC\Downloads\PythonProject3/flight-club\.venv\Lib\site-packages/requests/adapters.py", line 675, in send
    raise SSLError(e, request=request)
requests.exceptions.SSLError: HTTPSConnectionPool(host='api.sheety.co', port=443): Max retries exceeded with url: /b3890d6367f62b8d2568e931b76eb133/flightDeals/sheet1 (Caused by SSLError(SSLEOFError(8, '[SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1006)')))

Process finished with exit code 1

such error would mean you need network configuration, if you dont get such error, instead of the network file read section 2

#section 2

you can simply delete this network.py file then, instead of e,g...
from network import get_tls12_session
import os

class DataManager:
    SHEETY_PRICES_ENDPOINT = "https://api.sheety.co/b3890d6367f62b8d2568e931b76eb133/flightDeals/sheet1"

    def __init__(self):
        self.session = get_tls12_session()
        self.headers = {"Authorization": os.getenv("BASIC_KEY")}
        
then you simply use the get request as usual,, e.g...      
class DataManager:

    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        # Gets all the data from sheety, calls the actual sheet with the prices, in this case "sheet1"
        response = requests.get(url=SHEETY_PRICES_ENDPOINT,headers=headers, timeout=30, verify=False)
        data = response.json()
        self.destination_data = data["sheet1"]
        return self.destination_data 
'''

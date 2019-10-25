# python-cygrpc

## instalation

add in `requirements.txt` project file:
```requirements.txt
git+https://gitlab.com/cuembylabs/cyrpc/python-cyrpc.git#egg=cygrpc
```
**Note:** you need configure SSH key and gitconfig for access to private repository


## Usage

### Server
Params:

* host : str =  server host, by default is '0.0.0.0'
* port : int = server port for listen. by default is 50051
* max_threads : int =  set threads workers for server, by default is 10
* interceptors: tuple(InterceptorImplementation) = server interceptors middlewares. by default is None.
* http_port: int = port for http gateway 

if you decide used all values by default, you can setup the server in less lines
```python
from cygrpc.server import Server
server = Server()
server.add_service(calculator_api_pb2_grpc, ServiceImpl)
server.start()
```

Example using all params:
```python
from cygrpc.server import Server
# Initialization of server definition, 'host', 'port', 'max_threads' has be optionals.
# By default the __init__ function set the same values. if don't you wanna set interceptors only remove the param
server = Server(host="0.0.0.0", port=50051, max_threads=10, interceptors=(MyAuthInterceptor(),))

# attach service to server, repeat for multiple services
server.add_service(calculator_api_pb2_grpc, ServiceImpl)

# finally start server.
server.start()
```


### Implement service 
The implementation is the same.

```python
# import  rest decorator
from cygrpc.gateway.http import rest

class ServiceImpl(calculator_api_pb2_grpc.CalculatorAPIServicer):
    """
    Service logic implementation.
    """
    
    def Sum(self, request, context):
        total = 0
        for addend in request.addends:
            total += addend

        response = pb.SumResponse(sum=total)
        return response
```

#### rest route

for add rest route add the decorator @rest to method definition:

```python
# import rest decorator
from cygrpc.gateway.http import rest


class ServiceImpl(calculator_api_pb2_grpc.CalculatorAPIServicer):
    """
    Service logic implementation.
    """
    @rest("/v1/calculator/sum", method="POST")
    def Sum(self, request, context):
        total = 0
        for addend in request.addends:
            total += addend

        response = pb.SumResponse(sum=total)
        return response
```


### Interceptors

- Base Interceptor : Base interceptor implementation for create your custom interceptor

```python
from cygrpc.middleware import CyGrpcInterceptor

class CustomInterceptor(CyGrpcInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        # for continue to method implementation  
        return self.on_success(continuation, handler_call_details)
        # for terminate request
        return self.on_failed(grpc.StatusCode.UNAUTHENTICATED, "Validate authentication failed.")

```

- Authentication interceptor: provider a base for authentication middleware interceptor

```python
from cygrpc.middleware.auth import CyGrpcAuthInterceptor

class MyAuthInterceptor(CyGrpcAuthInterceptor):
    def auth_process(self, continuation, handler_call_details):
       """"
       ..... my auth validation process ....
       """
       return True
``` 


## Authors:
- Fabio Moreno <fabio.moreno@cuemby.com>
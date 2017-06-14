# built-in
from contextlib import ExitStack

# 3rd party
from sanic import Sanic
from sanic.exceptions import NotFound
from sanic.response import json
from sanic.views import HTTPMethodView
from sanic.request import Request
from sanic_cors import CORS, cross_origin
from multipledispatch import dispatch

# framework
from dorm.utils.serializers import ModelSerializer, SerializerMethod
from dorm.database.drivers.sqlite import Sqlite
from config import DATABASES

app = Sanic(name=__name__)
CORS(app)

# for all the 404 lets handle the exceptions
@app.exception(NotFound)
def ignore_404s(request, exception):
    return json({'method': request.method,
                 'status': exception.status_code,
                 'error': exception.args[0],
                 'results': None,
                 })

def rest(methods=[], databases=[]):
    """Add rest features:
        get_object: gets the instance of database model
        get: gets serialized database model
        put: inserts into database
        patch: updates model
        delete: deletes the model from database
    """
    def decorator(cls):
        """Generates sanic HTTPMethodView out of decorated class"""
        generic_name = cls.__name__
        generic_view = type(generic_name+"View", (HTTPMethodView,), {})
        generic_serializer = type(generic_name+"Serializer",
                                  (ModelSerializer,),
                                  {"model":cls, "_fields":cls.__fields__})
        setattr(generic_serializer, "Meta", type("Meta", (), {"_fields":cls.__fields__}))

         # I know what you see below is shameful but html methods are kinda static
        def add_method(view_, generic_serializer_):
            """Adds pre-defined methods to targer view"""
            
            def get_object(self, request, generic_id):
                """gets the instance of database model"""
                try:
                    # on database consults
                    generic_model = cls.select().where(**{'id': generic_id}).first()

                except Exception as ex:
                    raise NotFound(ex.args[0])
                return generic_model

            def get_objects(self, request):
                """gets the instance of database model"""
                try:
                    # on database consults
                    generic_model = cls.select().all()

                except Exception as ex:
                    raise NotFound(ex.args[0])
                return generic_model

            def get(self, request, generic_id=None):
                """Gets the model from database and serializes it."""
                if generic_id:
                    # on database consults
                    generic_model = self.get_object(request, generic_id)

                    return json({'method': request.method,
                                'status': 200,
                                'results': generic_serializer_.serialize(generic_model),
                                })
                else:
                    generic_model = self.get_objects(request)

                    return json({'method': request.method,
                                'status': 200,
                                'results': generic_serializer_.serialize(generic_model),
                                })

            def put(self, request, generic_id):
                """Creates a generic model with given parameters and saves it."""
                # on database consults
                generic_model = self.get_object(request, generic_id)
                # on save
                generic_model.save(**request.json)

                return json({'method': request.method,
                             'status': 200,
                             'results': generic_serializer_.serialize(generic_model),
                            })

            def patch(self, request, generic_id):
                """Update model with given parameters"""
                # on database consults
                generic_model = self.get_object(request, generic_id)
                # on save
                generic_model.save(**request.json)

                return json({'method': request.method,
                             'status': 200,
                             'results': generic_serializer_.serialize(generic_model),
                            })

            def delete(self, request, generic_id):
                """Delete model from database"""
                # on database consults
                generic_model = self.get_object(request, generic_id)
                # on its deletion
                generic_model.delete()

                return json({'method': request.method,
                             'status': 200,
                             'results': None
                            })
            def arg_parser(self, request):
                """Parse the request args"""
                parsed_args = {}
                for key, val in request.args.items():
                    parsed_args[key] = val[0]
                return parsed_args
            # add arg parser to generic view
            setattr(view_, "arg_parser", arg_parser)

           
            for method in ["get_object", "get", "put", "patch", "delete", "get_objects"]:
                if method in methods:
                    continue
                elif method == "get_object":
                    setattr(view_, method, get_object)
                elif method == "get_objects":
                    setattr(view_, method, get_objects)
                elif method == "get":
                    setattr(view_, method, get)
                elif method == "put":
                    setattr(view_, method, put)
                elif method == "patch":
                    setattr(view_, method, patch)
                elif method == "delete":
                    setattr(view_, method, delete)
            return view_

        generic_view = add_method(generic_view, generic_serializer)
        app.add_route(generic_view.as_view(), '/'+generic_name.lower()+'/')
        print('/'+generic_name.lower()+'/')
        app.add_route(generic_view.as_view(), '/'+generic_name.lower()+'/'+'<'+'generic_id:int>/')
        return cls
    return decorator

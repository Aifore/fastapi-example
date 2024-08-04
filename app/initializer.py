from inspect import getmembers

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter as grpc_exporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.tortoiseorm import TortoiseORMInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from tortoise.contrib.starlette import register_tortoise

from config import tortoise_config
from core.routers.items import router
from utils.api.router import TypedAPIRouter


def init(app: FastAPI):
    """
    Init routers and etc.
    :return:
    """
    init_otle(app)
    init_routers(app)
    # include_router(router)
    init_db(app)
    init_exceptions_handlers(app)


def init_exceptions_handlers(app: FastAPI):
    from core.exceptions.handlers import tortoise_exception_handler
    from core.exceptions.handlers import BaseORMException

    app.add_exception_handler(BaseORMException, tortoise_exception_handler)


def init_db(app: FastAPI):
    """
    Init database models.
    :param app:
    :return:
    """
    register_tortoise(
        app,
        db_url=tortoise_config.db_url,
        generate_schemas=tortoise_config.generate_schemas,
        modules=tortoise_config.modules,
    )


def init_routers(app: FastAPI):
    """
    Initialize routers defined in `api`
    :param app:
    :return:
    """
    from core import routers

    routers = [o[1] for o in getmembers(routers) if isinstance(o[1], TypedAPIRouter)]

    for router in routers:
        app.include_router(**router.dict())


def init_otle(app: FastAPI):
    # set the tracer provider
    resource = Resource(attributes={
        "service.name": "linlin7"
    })
    tracer = TracerProvider(resource=resource)
    tracer.add_span_processor(
        BatchSpanProcessor(
            grpc_exporter(endpoint="http://jaegertracing:4317")
        )
    )
    trace.set_tracer_provider(tracer)
    FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer)
    TortoiseORMInstrumentor().instrument(tracer_provider=tracer)
    print("Tracer initialized")

from django_xmlrpc.dispatcher import DjangoXMLRPCDispatcher
from tapatalk import settings


# If we need to debug, now we know
DEBUG = hasattr(settings, 'XMLRPC_DEBUG') and settings.XMLRPC_DEBUG


class TapatalkXMLRPCDispatcher(DjangoXMLRPCDispatcher):
    def _marshaled_dispatch(self, request, django_args, django_kwargs):
        def dispatch_method(method, params):
            try:
                func = self.funcs[method]
            except KeyError:
                raise Exception('method "%s" is not supported' % method)

            kwargs = {}
            if django_args:
                kwargs['django_args'] = django_args
            if django_kwargs:
                kwargs['django_kwargs'] = django_kwargs
            return func(request, *params, **kwargs)

        # Tapatalk sends out bad formatted booleans... *sigh*
        body = request.raw_post_data.replace('<boolean>true</boolean>', '<boolean>1</boolean>')

        return DjangoXMLRPCDispatcher._marshaled_dispatch(self, body, dispatch_method)

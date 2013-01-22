from tapatalk import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt

from dispatcher import TapatalkXMLRPCDispatcher, DjangoXMLRPCDispatcher


# We create a local DEBUG variable from the data in settings.
DEBUG = hasattr(settings, 'XMLRPC_DEBUG') and settings.XMLRPC_DEBUG
DEBUG = True

# Declare xmlrpcdispatcher correctly depending on our python version
xmlrpcdispatcher = TapatalkXMLRPCDispatcher(allow_none=False, encoding=None)


@csrf_exempt
def handle_xmlrpc(request, *args, **kwargs):
    if request.method == "POST":
        if DEBUG:
            print request.body
        try:
            response = HttpResponse(content_type='text/xml')
            response.write(xmlrpcdispatcher._marshaled_dispatch(request, args, kwargs))
            if DEBUG:
                print response
            return response
        except:
            return HttpResponseServerError()


# Load up any methods that have been registered with the server in settings
if hasattr(settings, 'TAPATALK_METHODS'):
    for path, name in settings.TAPATALK_METHODS:
        # if "path" is actually a function, just add it without fuss
        print path
        if callable(path):
            xmlrpcdispatcher.register_function(path, name)
            continue

        # Otherwise we try and find something that we can call
        i = path.rfind('.')
        module, attr = path[:i], path[i + 1:]

        try:
            mod = __import__(module, globals(), locals(), [attr])
        except ImportError, ex:
            raise ImproperlyConfigured("Error registering XML-RPC method: " \
                + "module %s can't be imported" % module)

        try:
            func = getattr(mod, attr)
        except AttributeError:
            raise ImproperlyConfigured('Error registering XML-RPC method: ' \
                + 'module %s doesn\'t define a method "%s"' % (module, attr))

        if not callable(func):
            raise ImproperlyConfigured('Error registering XML-RPC method: ' \
                + '"%s" is not callable in module %s' % (attr, module))

        xmlrpcdispatcher.register_function(func, name)


# Finally, register the introspection and multicall methods with the XML-RPC
# namespace
xmlrpcdispatcher.register_introspection_functions()
xmlrpcdispatcher.register_multicall_functions()

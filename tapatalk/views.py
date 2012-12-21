from django_xmlrpc.views import *
from tapatalk import settings

# Load up any methods that have been registered with the server in settings
if hasattr(settings, 'TAPATALK_METHODS'):
    for path, name in settings.TAPATALK_METHODS:
        # if "path" is actually a function, just add it without fuss
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

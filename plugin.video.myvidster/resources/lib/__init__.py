from . import vidster, simpleplugin, gifmaker
try:
    from . import urlquick
    Get = urlquick.get
except:
    Get = None
Plugin = simpleplugin.Plugin
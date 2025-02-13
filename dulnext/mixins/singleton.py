class SingletonMixin:
    """Singleton mixin"""

    __instance = None

    def __init__(self):
        """Creates a new singlton object"""
        impl = getattr(self.__class__, "_%s__impl" % self.__class__.__name__)

        if self.__class__.__instance is None:
            self.__class__.__instance = impl()

        setattr(
            self.__class__,
            "_%s__instance" % self.__class__.__name__,
            self.__class__.__instance,
        )

    def __getattr__(self, attr):
        """Delegate access to implementation"""
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """Delegate access to implementation"""
        return setattr(self.__instance, attr, value)

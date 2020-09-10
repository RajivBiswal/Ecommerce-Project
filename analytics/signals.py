from django.dispatch import Signal

object_viewed_signal = Signal(providing_args=['instance','request'])


class ObjectViewedMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super(ObjectViewedMixin, self).get_context_data(*args, **kwargs) #data of class it inherting from
        request = self.request
        instance = context.get('object')    #geting the context object
        if instance:
            object_viewed_signal.send(instance.__class__, instance=instance, request=request) #(sender,object,request)
        return context

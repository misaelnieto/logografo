import grok

from logografo import resource

class Logografo(grok.Application, grok.Container):
    pass

class Index(grok.View):
    def update(self):
        resource.style.need()

import grok

class DoAnything(grok.Permission):
    grok.name('logografo.DoAnything')
    
class Administrator(grok.Role):
    grok.name('logografo.Administrator')
    grok.title('Administrator')
    grok.permissions(DoAnything)
    
    
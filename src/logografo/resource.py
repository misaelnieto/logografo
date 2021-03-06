from fanstatic import Library, Resource

#Library
library = Library('logografo', 'static')

#Resources
style = Resource(library, 'style.css')
listing_css = Resource(library, 'listing.css')

logografo_timeline = Resource(library, 'logografo_timeline.js')
jquery_min = Resource(library, 'jquery-1.6.2.min.js')
vtip = Resource(library, 'vtip.js')
listing_js = Resource(library, 'listing.js')
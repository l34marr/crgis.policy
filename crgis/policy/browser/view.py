from zope.interface import implements
from zope.component import getMultiAdapter
from Acquisition import aq_inner

from plone.memoize.instance import memoize
from plone.app.layout.navigation.root import getNavigationRootObject

from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five import BrowserView

from crgis.policy.interfaces import IFrontPage


class FrontPage(BrowserView):

    implements(IFrontPage)

    def latest_news(self):
        return self._news()

    def latest_events(self):
        return self._event()

    @memoize
    def _news(self):
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        portal_state = getMultiAdapter((context, self.request),
            name=u'plone_portal_state')
        path = portal_state.navigation_root_path() + '/info/news'
        return catalog(portal_type='News Item',
                       review_state='published',
                       path=path,
                       sort_on='effective',
                       sort_order='reverse',
                       sort_limit=5)[:5]

    def _event(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        portal_state = getMultiAdapter((context, self.request),
            name=u'plone_portal_state')
        path = portal_state.navigation_root_path() + '/info/events'
        return catalog(portal_type='Event',
                       review_state=('external', 'internal', 'internally_published', 'published'),
                       path=path,
                       sort_on='start',
                       sort_order='reverse',
                       sort_limit=5)[:5]

    def allNewsURL(self):
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request),
            name=u'plone_portal_state')
        return portal_state.navigation_root_path() + '/info/news'

    def allEventURL(self):
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request),
            name=u'plone_portal_state')
        return portal_state.navigation_root_path() + '/info/events'


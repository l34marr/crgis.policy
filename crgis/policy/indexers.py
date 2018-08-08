#!/usr/bin/python
# -*- coding: utf-8 -*-

from Acquisition import aq_base
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from plone.indexer.decorator import indexer
from plone.app.contenttypes.indexers import _unicode_save_string_concat
from plone.app.contenttypes.indexers import SearchableText
from Products.CMFPlone.utils import safe_unicode
from BeautifulSoup import BeautifulSoup as bs
from crgis.content.interfaces import IDaoShi
from crgis.content.interfaces import IDaoFaTan
from crgis.content.interfaces import IKeYi
from crgis.content.interfaces import IBanHua
from crgis.content.interfaces import IBuddhist
try:
    from crgis.atcontents.interfaces.temple import ITemple
except ImportError:
    from crgis.content.interfaces import ITemple
try:
    from crgis.atcontents.interfaces import IBiXieWu
except ImportError:
    from crgis.content.interfaces import IBiXieWu


@indexer(ITemple)
def deity_main(obj, **kw):
    results = []
    factory = getUtility(IVocabularyFactory, 'deity_name')
    vocabulary = factory(obj)
    if obj.deity_host == None:
        return None
    for value in obj.deity_host:
        try:
            existing = vocabulary.getTerm(value)
            results.append(existing.title.split(u': ')[0].encode('utf8'))
        except LookupError:
            if value == u'福德正神': value = u'土地公'
            if value == u'開台聖王(鄭成功)': value = u'鄭成功'
            results.append(value)
    return results

@indexer(ITemple)
def deity(obj, **kw):
    results = []
    factory = getUtility(IVocabularyFactory, 'deity_name')
    vocabulary = factory(obj)
    for value in (set(obj.deity_host) | set(obj.deity_company)):
        try:
            existing = vocabulary.getTerm(value)
            results.append(existing.title.split(u': ')[0].encode('utf8'))
        except LookupError:
            results.append(value)
    return results

@indexer(ITemple)
def wynm(obj):
    results = []
    if obj.wysm == None: return None
    for value in obj.wysm.split(u';'):
        if value == u'': continue
        results.append(u''.join(value.split(u',')))
    return results

@indexer(ITemple)
def area1_temple(obj):
    return obj.__parent__.__parent__.Title()

@indexer(IBuddhist)
def area1_buddhist(obj):
    return obj.area

@indexer(ITemple)
def area2(obj):
    return obj.__parent__.__parent__.Title() + obj.__parent__.Title()

@indexer(ITemple)
def hostcmpn(obj):
    results = []
    host = obj.deity_host
    cmpn = obj.deity_company
    if 'deity_001' in host or '\xe7\x8e\x8b\xe7\x88\xba' in host:
        results.append('hwy')
    if 'deity_001' in cmpn or '\xe7\x8e\x8b\xe7\x88\xba' in cmpn:
        results.append('cwy')
    if 'deity_005' in host or '\xe5\xa4\xa9\xe4\xb8\x8a\xe8\x81\x96\xe6\xaf\x8d' in host or '\xe5\xaa\xbd\xe7\xa5\x96' in host:
        results.append('hmz')
    if 'deity_005' in cmpn or '\xe5\xa4\xa9\xe4\xb8\x8a\xe8\x81\x96\xe6\xaf\x8d' in cmpn or '\xe5\xaa\xbd\xe7\xa5\x96' in cmpn:
        results.append('cmz')
    if 'deity_008' in host or '\xe7\x8e\x84\xe5\xa4\xa9\xe4\xb8\x8a\xe5\xb8\x9d' in host:
        results.append('hxt')
    if 'deity_008' in cmpn or '\xe7\x8e\x84\xe5\xa4\xa9\xe4\xb8\x8a\xe5\xb8\x9d' in cmpn:
        results.append('cxt')
    return results

@indexer(ITemple)
def founded(obj):
    if obj.era is None or obj.era == '':
        return None
    else:
        try:
            return int(obj.era)
        except ValueError:
            return None

@indexer(IDaoShi)
def dt_type_shi(obj):
    if obj.dt_type == tuple():
        pass
    else:
        return obj.dt_type[0]

@indexer(IDaoFaTan)
def dt_type_tan(obj):
    if obj.dt_type == tuple():
        pass
    else:
        return obj.dt_type[0]

@indexer(IKeYi)
def leibie_keyi(obj):
    if obj.leibie == tuple():
        return None
    else:
        return obj.leibie[0]

@indexer(IDaoFaTan)
def chngyn(obj):
    if obj.aq_base.chngyn == tuple():
        return tuple()
    return tuple(safe_unicode(s.to_object.Title()) for s in obj.aq_base.chngyn)

@indexer(IDaoShi)
def shchn_shi(obj):
    if obj.aq_base.shchn == tuple():
        return tuple()
    return tuple(safe_unicode(s.to_object.Title()) for s in obj.aq_base.shchn)

@indexer(IDaoFaTan)
def shchn_tan(obj):
    if obj.aq_base.shchn == tuple():
        return tuple()
    return tuple(safe_unicode(s.to_object.Title()) for s in obj.aq_base.shchn)

@indexer(IBiXieWu)
def purpose(obj):
    return obj.purpose

@indexer(IBiXieWu)
def material(obj):
    return obj.material

@indexer(IBiXieWu)
def locational(obj):
    return obj.locational

@indexer(IBiXieWu)
def color(obj):
    return obj.color

@indexer(IBiXieWu)
def genre(obj):
    return obj.genre

@indexer(IBiXieWu)
def posture(obj):
    return obj.posture

@indexer(IBiXieWu)
def gender(obj):
    return obj.gender

@indexer(IBiXieWu)
def lct_cou(obj):
    return obj.lct_cou

@indexer(IBiXieWu)
def lct_tow(obj):
    return obj.lct_tow

@indexer(IBiXieWu)
def lct_vil(obj):
    return obj.lct_vil

@indexer(IBiXieWu)
def height(obj):
    if obj.shi_h:
        try:
            value = int(obj.shi_h)
        except ValueError:
            value = None
    else:
        value = None
    return value

@indexer(IBanHua)
def SearchableText_banhua(obj):
    return _unicode_save_string_concat(SearchableText(obj))

@indexer(IBuddhist)
def leibie_buddhist(obj):
    if obj.fenlei:
        return obj.fenlei
    else:
        return None


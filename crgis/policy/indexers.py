#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from plone.indexer.decorator import indexer
from BeautifulSoup import BeautifulSoup as bs
from Products.ATContentTypes.interfaces import IATDocument
try:
    from crgis.atcontents.interfaces.temple import ITemple
except ImportError:
    from crgis.content.interfaces import ITemple
try:
    from crgis.atcontents.interfaces import IBiXieWu
except ImportError:
    from crgis.content.interfaces import IBiXieWu

#from crgis.content.theater import ITheater
#from crgis.content.liuyu import ILiuYu


#@indexer(IATDocument)
#def portal_type(obj):
#    if obj.__parent__.getId() == 'bgis':
#        return 'Buddhist'

@indexer(IATDocument)
def bgis_type(obj):
    if obj.__parent__.getId() == 'bgis':
        try:
            k, v = bs(obj.getText()).find('p', {'class': 'ct'}).text.split(': ')
            if k == u'分類': return v
        except ValueError:
            pass

@indexer(IATDocument)
def area1_bgis(obj):
    if obj.__parent__.getId() == 'bgis':
        k, v = bs(obj.getText()).find('p', {'class': 'pr'}).text.split(': ')
        if k == u'省': return v

@indexer(ITemple)
def deity_main(obj, **kw):
    results = []
    factory = getUtility(IVocabularyFactory, 'deity_name')
    vocabulary = factory(obj)
    for value in obj.getDeity_host():
        try:
            existing = vocabulary.getTerm(value)
            results.append(existing.title.split(u': ')[0].encode('utf8'))
        except LookupError:
            results.append(value)
    return results

@indexer(ITemple)
def deity(obj, **kw):
    results = []
    factory = getUtility(IVocabularyFactory, 'deity_name')
    vocabulary = factory(obj)
    for value in (set(obj.getDeity_host()) | set(obj.getDeity_company())):
        try:
            existing = vocabulary.getTerm(value)
            results.append(existing.title.split(u': ')[0].encode('utf8'))
        except LookupError:
            results.append(value)
    return results

@indexer(ITemple)
def wynm(obj):
    results = []
    for value in obj.getWysm().split(u';'):
        if value == u'': continue
        results.append(u''.join(value.split(u',')))
    return results

@indexer(ITemple)
def area1_temple(obj):
    return obj.__parent__.__parent__.Title()

@indexer(ITemple)
def area2(obj):
    return obj.__parent__.__parent__.Title() + obj.__parent__.Title()

@indexer(ITemple)
def hostcmpn(obj):
    results = []
    host = obj.getDeity_host()
    cmpn = obj.getDeity_company()
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
    if obj.era == '':
        pass
    else:
        try:
            return int(obj.era)
        except ValueError:
            pass

#@indexer(ITheater)
#def adm_area(obj):
#    return obj.adm_area

#@indexer(ITheater)
#def function(obj):
#    return obj.function

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

#@indexer(ITheater)
#def owner(obj):
#    return obj.owner

#@indexer(ITheater)
#def operator(obj):
#    return obj.operator

#@indexer(ITheater)
#def in_charge(obj):
#    return obj.in_charge

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

#@indexer(ILiuYu)
#def time_start(obj):
#    if obj.year_start:
#        try:
#            time = int(obj.year_start)
#        except ValueError:
#            time = None
#    else:
#        time = None
#    return time

#@indexer(ILiuYu)
#def country(obj):
#    return obj.country

#@indexer(ILiuYu)
#def state(obj):
#    return obj.state

#@indexer(ILiuYu)
#def city(obj):
#    return obj.city

#@indexer(ILiuYu)
#def county(obj):
#    return obj.county

#@indexer(ILiuYu)
#def river(obj):
#    return obj.river

#@indexer(ILiuYu)
#def mountain(obj):
#    return obj.mountain

#@indexer(ILiuYu)
#def monastery(obj):
#    return obj.monastery

#@indexer(ILiuYu)
#def tomb(obj):
#    return obj.tomb

#@indexer(ILiuYu)
#def castle(obj):
#    return obj.castle

#@indexer(ILiuYu)
#def fortress(obj):
#    return obj.fortress

#@indexer(ILiuYu)
#def relices(obj):
#    return obj.relices

#@indexer(ILiuYu)
#def buildings(obj):
#    return obj.buildings

#@indexer(ILiuYu)
#def legend(obj):
#    return obj.legend

#@indexer(ILiuYu)
#def people(obj):
#    return obj.people.raw

#@indexer(ILiuYu)
#def ref_name(obj):
#    return obj.ref_name


#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from plone.indexer.decorator import indexer
from crgis.atcontents.interfaces.temple import ITemple
from crgis.content.theater import ITheater
from crgis.content.liuyu import ILiuYu
from crgis.atcontents.interfaces import IBiXieWu


@indexer(ITemple)
def deity_main(object, **kw):
    results = []
    factory = getUtility(IVocabularyFactory, 'deity_name')
    vocabulary = factory(object)
    for value in object.getDeity_host():
        try:
            existing = vocabulary.getTerm(value)
            results.append(existing.title.split(u'\uff0c')[0])
        except LookupError:
            results.append(value)
    return results

@indexer(ITemple)
def founded(obj):
    return obj.era

@indexer(ITheater)
def adm_area(obj):
    return obj.adm_area

@indexer(ITheater)
def function(obj):
    return obj.function

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

@indexer(ITheater)
def owner(obj):
    return obj.owner

@indexer(ITheater)
def operator(obj):
    return obj.operator

@indexer(ITheater)
def in_charge(obj):
    return obj.in_charge

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

@indexer(ILiuYu)
def time_start(obj):
    if obj.year_start:
        try:
            time = int(obj.year_start)
        except ValueError:
            time = None
    else:
        time = None
    return time

@indexer(ILiuYu)
def country(obj):
    return obj.country

@indexer(ILiuYu)
def state(obj):
    return obj.state

@indexer(ILiuYu)
def city(obj):
    return obj.city

@indexer(ILiuYu)
def county(obj):
    return obj.county

@indexer(ILiuYu)
def river(obj):
    return obj.river

@indexer(ILiuYu)
def mountain(obj):
    return obj.mountain

@indexer(ILiuYu)
def monastery(obj):
    return obj.monastery

@indexer(ILiuYu)
def tomb(obj):
    return obj.tomb

@indexer(ILiuYu)
def castle(obj):
    return obj.castle

@indexer(ILiuYu)
def fortress(obj):
    return obj.fortress

@indexer(ILiuYu)
def relices(obj):
    return obj.relices

@indexer(ILiuYu)
def buildings(obj):
    return obj.buildings

@indexer(ILiuYu)
def legend(obj):
    return obj.legend

@indexer(ILiuYu)
def people(obj):
    return obj.people.raw

@indexer(ILiuYu)
def ref_name(obj):
    return obj.ref_name


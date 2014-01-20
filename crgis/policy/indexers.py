#!/usr/bin/python
# -*- coding: utf-8 -*-

from plone.indexer.decorator import indexer
from crgis.atcontents.interfaces.temple import ITemple
from crgis.content.theater import ITheater


@indexer(ITemple)
def deity_main(object, **kw):
    results = []
    factory = getUtility(IVocabularyFactory, 'deity_name')
    vocabulary = factory(object)
    for value in object.getDeity_host():
        try:
            existing = vocabulary.getTerm(value)
            results.append(existing.title.split('，')[0])
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

@indexer(ITheater)
def owner(obj):
    return obj.owner

@indexer(ITheater)
def operator(obj):
    return obj.operator

@indexer(ITheater)
def in_charge(obj):
    return obj.in_charge


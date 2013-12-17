from plone.indexer.decorator import indexer
from crgis.content.theater import ITheater


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


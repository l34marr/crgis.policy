from plone.indexer.decorator import indexer
from crgis.content.theater import ITheater


@indexer(ITheater)
def adm_area(obj):
    return obj.adm_area


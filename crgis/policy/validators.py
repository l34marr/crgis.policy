# -*- coding: utf-8 -*-
from plone.namedfile.interfaces import INamedBlobImageField
from plone.app.contenttypes.interfaces import IImage
from zope.interface import Invalid
from z3c.form import validator


# 2 MB size limit
MAXSIZE = 2 * 1024 * 1024


class ImageFileSizeValidator(validator.FileUploadValidator):

    def validate(self, value):
        super(ImageFileSizeValidator, self).validate(value)

        if value.getSize() > MAXSIZE:
            raise Invalid("Image is too large")


validator.WidgetValidatorDiscriminators(ImageFileSizeValidator,
                                        context=IImage,
                                        field=INamedBlobImageField)


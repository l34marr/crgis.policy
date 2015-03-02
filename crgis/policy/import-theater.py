#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Testing import makerequest
root = makerequest.makerequest(app)
site = root.crgis

admin = root.acl_users.getUserById('admin')
admin = admin.__of__(site.acl_users)

from AccessControl.SecurityManagement import newSecurityManager
newSecurityManager(None, admin)

from zope.site.hooks import setHooks
from zope.site.hooks import setSite
setHooks()
setSite(site)
site.setupCurrentSkin(site.REQUEST)

folder = site.assets.tangible.f_building['theater']

import csv
from plone.dexterity.utils import createContentInContainer

with open('theater.csv', 'rb') as f:
    #dialect = csv.Sniffer().sniff(f.read(1024), delimiters=";")
    f.seek(0)
    reader = csv.reader(f) #, dialect)
    for row in reader:
        item = createContentInContainer(folder, 'Theater', title=row[1], adm_area=row[2], address=row[3], owner=row[4], operator=row[5], in_charge=row[6], contract=row[7], checkConstraints=False)
#       folder.manage_renameObject(item.getId(), str(row[3]))

import transaction
transaction.commit()

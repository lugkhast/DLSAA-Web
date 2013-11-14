
from google.appengine.ext import ndb

# DLSAA Card partner locator stuff
# ---------------------------------------------------------


class PartnerBusiness(ndb.Model):
    name = ndb.StringProperty()
    discount_description = ndb.StringProperty()

    def to_dict(self):
        business_dict = {}
        business_dict['name'] = self.name
        business_dict['discount_description'] = self.discount_description

        return business_dict


class PartnerBranch(ndb.Model):
    address = ndb.StringProperty()
    location = ndb.GeoPtProperty()


# Chapter locator
# ---------------------------------------------------------


class Chapter(ndb.Model):
    name = ndb.StringProperty()
    has_address = ndb.BooleanProperty()
    address = ndb.StringProperty()


class Officer(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()
    mobile_number = ndb.StringProperty()


# News and events
# ---------------------------------------------------------
class NewsArticle(ndb.Model):
    title = ndb.StringProperty()
    body = ndb.StringProperty()

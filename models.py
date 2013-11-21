
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
        business_dict['id'] = self.key.urlsafe()

        branches = PartnerBranch.query(PartnerBranch.business_key == self.key)
        branch_dicts = [b.to_dict() for d in branches]
        business_dict['branches'] = branch_dicts

        return business_dict


class PartnerBranch(ndb.Model):
    address = ndb.StringProperty()
    location = ndb.GeoPtProperty()
    business_key = ndb.KeyProperty(kind='PartnerBusiness')

    def to_dict(self):
        branch_dict = {}
        branch_dict['address'] = self.address
        branch_dict['latitude'] = self.location.lat
        branch_dict['longitude'] = self.location.long

        branch_dict['business_key'] = self.business_key.urlsafe()

        return branch_dict


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

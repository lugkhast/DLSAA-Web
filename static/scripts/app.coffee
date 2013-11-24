 
window.App = App = Ember.Application.create()

App.Router.map ->
    this.resource 'businesses', ->
        this.resource 'business', { path: '/:business_id' }
        this.route 'new'

App.BusinessesRoute = Ember.Route.extend
    model: ->
        return App.Business.findAll()

App.BusinessRoute = Ember.Route.extend
    model: (params) ->
        return App.Business.findById(params.business_id)

App.BusinessController = Ember.ObjectController.extend
    newBranchDataIncomplete: ->
        incomplete = false

        address = this.get 'newAddress'
        latitude = this.get 'newLatitude'
        longitude = this.get 'newLongitude'

        if address == ''
            incomplete = true

        # Latitude is 0 at the equator and 90 at the poles. Negative to
        # represent the southern hemisphere. The given value must fall in this
        # range.
        if not (-90 <= latitude <= 90)
            incomplete = true

        # Longitude is 0 at the Prime Meridian, up to 180 towards the east, and
        # up to -180 towards the west.
        if not (-180 <= longitude <= 180)
            incomplete = true

        console.log 'Incomplete? ', incomplete
        return incomplete

    actions:
        updateBusiness: ->
            toastr.info 'Saving...'

            model = this.get 'model'
            model.save()

        showDeleteBusinessDialog: ->
            $('#deleteBusinessModal').modal('show')

        deleteBusiness: ->
            model = this.get 'model'
            App.Business.deleteInstance model
            this.transitionToRoute 'businesses'

        geocode: ->
            console.log 'TODO: Implement geocoding'

        reverseGeocode: ->
            console.log 'TODO: Implement reverse geocoding'

        addBranch: ->
            branch = App.Branch.create()
            branch.set 'address', this.get 'newAddress'
            branch.set 'latitude', this.get 'newLatitude'
            branch.set 'longitude', this.get 'newLongitude'
            branch.set 'business_key', this.get 'id'

            controller = this
            branch.save().success ->
                business = controller.get 'model'
                business.branches.push branch

App.BusinessesNewController = Ember.Controller.extend
    clearFields: ->
        this.set 'name', ''
        this.set 'discount_description', ''

    actions:
        addBusiness: ->
            toastr.info 'Saving...'

            business = App.Business.create()
            business.name = this.get 'name'
            business.discount_description = this.get 'discount_description'

            controller = this
            business.save().success ->
                controller.clearFields()
                console.log 'AAAAAAAAAAAAAAAAAAAAA', business
                controller.transitionToRoute 'business', business

 
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
    actions:
        save: ->
            toastr.info 'Saving...'

            model = this.get 'model'
            $.post('/api/business', JSON.stringify(model)).then (blah) ->
                console.log 'Posted!', blah

        showDeleteBusinessDialog: ->
            $('#deleteBusinessModal').modal('show')

        deleteBusiness: ->
            model = this.get 'model'
            App.Business.deleteInstance model
            this.transitionToRoute 'businesses'

App.BusinessesNewController = Ember.Controller.extend
    actions:
        addBusiness: ->
            toastr.info 'Saving...'

            business = App.Business.create()
            business.name = this.get 'name'
            business.discount_description = this.get 'discount_description'

            controller = this
            business.save().success ->
                console.log 'AAAAAAAAAAAAAAAAAAAAA', business
                controller.transitionToRoute 'business', business

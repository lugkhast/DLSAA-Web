 
window.App = App = Ember.Application.create()

window.dummy_businesses =
   businesses: [
       {
           name: 'Hello World Hotel and Resort'
           discount_description: '100% more hello world'
           id: '23ouf3i3'
           branches: [
               {
                   address: "123 Example Avenue, District, City"
                   latitude: 120.123456
                   longitude: 14.789012,
                   id: 'blarghlkw'
               },
               {
                   address: "999 Blahblah Road, Malate, Manila"
                   latitude: 40.123456
                   longitude: 14.789012
                   id: '2092f9'
               }
           ]
       },
       {
           name: 'Subs to Go'
           discount_description: 'OM NOM NOM WOW AHAHAHAHA'
           id: 'erugh949gh94hg'
           branches: [
               {
                   address: "2345 Example Avenue, District, City",
                   latitude: 120.123456,
                   longitude: 99.789012,
                   id: 'blarghlkw'
               }
           ]
       }
   ]


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

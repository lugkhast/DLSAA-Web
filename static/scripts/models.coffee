
# A hand-rolled persistence layer
# =============================================================================
# 
# Neither Ember Model nor Ember Data were cooperating, so here is a simple,
# custom-made layer for working with our API. 

# Ember Data uses what it calls an "Identity Map" for ensuring that only one
# copy of a particular object needs to be retrieved from the server. This also
# makes sure that all displayed data on that object is consistent across the
# app.
# 
# This implements that.
App.IdentityMap = Ember.Object.extend
    loadedModels: Ember.ArrayProxy.create
        content: []

    hasData: false

    setModels: (newModels) ->
        console.log 'Setting models to', newModels
        models = this.get 'loadedModels'
        models.set 'content', newModels
        this.set 'hasData', true
        console.log this.get('loadedModels')

    putModel: (newModel) ->
        models = this.get 'loadedModels'
        models.addObject newModel

    findById: (id) ->
        return this.get('loadedModels').findBy 'id', id

    findAll: ->
        return this.get 'loadedModels'

    deleteModel: (model) ->
        # removeObject appears to want the exact object for it to do the removal
        # Let's get crafty!

        models = this.get 'loadedModels'

        # This makes sure we get the exact copy that's in the Ember.Array
        modelToRemove = this.findById model.id

        models.removeObject modelToRemove

    init: ->
        console.log 'IdentityMap created!'



App.Model = Ember.Object.extend()

App.Model.reopenClass({
    checkRequiredProperties: ->
        if not (this.url and this.collectionKey and this.rootKey)
            throw new Error('Model subclasses require url, collectionKey and rootKey properties')

    findAll: ->
        this.checkRequiredProperties()

        # Grab data from the identity map if it's there
        this.identityMap = this.identityMap or App.IdentityMap.create()
        imap = this.identityMap
        if imap.get 'hasData'
            # Models retrieved from the identity map must be wrapped within a
            # Promise.
            console.debug 'CACHED - retrieving data from identity map'
            return new Ember.RSVP.Promise (resolve, reject) ->
                resolve imap.findAll()

        if not this.url
            throw new Error("App.Model subclasses need a url property")

        console.debug 'NOT CACHED - retrieving data from server'
        collectionKey = this.collectionKey
        modelClass = this
        return $.getJSON(this.url).then (data) ->
            # Instantiate instances of the appropriate class, so we can use its
            # methods later
            models = (modelClass.create(obj) for obj in data[collectionKey])
            imap.setModels models

            # We need to return the identity map's copy, so deletions/other
            # modifications to the backing array result in events that everyone
            # can react to.
            return imap.findAll()

    findById: (id) ->
        # If it's in the identity map, use that
        this.identityMap = this.identityMap or App.IdentityMap.create()
        imap = this.identityMap
        if imap.get('hasData') and (model = imap.findById(id))
            # Models retrieved from the identity map must be wrapped within a
            # Promise.
            return new Ember.RSVP.Promise (resolve, reject) ->
                resolve model

        # Otherwise, go to the server to get it
        return $.getJSON(this.url + id).then (data) ->
            model = this.create(data[this.rootKey])
            imap.putModel model

            return model

    deleteInstance: (model) ->
        imap = (this.identityMap or App.IdentityMap.create())

        return $.ajax(
            type: 'DELETE'
            url: "#{this.url}/#{model.id}"
            contentType: 'application/json'
        ).success(
            # Only remove the model if the deletion was successful
            console.log 'Removing model...', model
            imap.deleteModel model
        )

    reload: (newData) ->
        if newData
            # If we're given data, just pass that to the identity map
            this.identityMap.setModels newData
        else
            # Ask for all models again
            this.identityMap.set('hasData', false)
            this.findAll()
})


App.Model.reopen
    update: ->
        if not this.id
            throw Error('Need an id to call update!')

        model = this
        modelClass = this.constructor
        return $.ajax(
            type: 'PUT'
            url: "#{modelClass.url}/#{this.id}"
            data: JSON.stringify(model)
            contentType: 'application/json'
        ).success (data) ->
            console.log 'PUT successful', data

    save: ->
        if this.id
            this.update()
            return

        model = this
        modelClass = this.constructor
        return $.ajax(
            type: 'POST'
            url: modelClass.url
            data: JSON.stringify(model)
            contentType: 'application/json'
        ).success (data) ->
            console.log 'Success!', data
            data = JSON.parse(data)
            model.id = data.key

            # Add the model to the identity map
            imap = modelClass.identityMap
            imap.putModel model


App.Business = App.Model.extend
    name: null
    discount_description: null
    branches: []

    id: null

App.Business.url = '/api/business'
App.Business.rootKey = 'business'
App.Business.collectionKey = 'businesses'
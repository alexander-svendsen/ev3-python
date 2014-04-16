
define([
    'jquery',
    'underscore',
    'backbone',
    'collections/sensor',
    'text!templates/app.html',
    'text!templates/header.html',
    'bootstrap'
], function($, _, Backbone, SensorCollection, template, HeaderTemplate, bootstrap){
    var AppView = Backbone.View.extend({
        el: '#app',

        header_template : _.template(HeaderTemplate),

        //Set up the bindings and such here
        initialize: function () {
            this.$el.append(this.header_template); //render header

            this.available_bricks = $('#available_bricks');

            this.collection = new SensorCollection();
            this.collection.add({ name: "EV3UltraSonic?"});
            this.collection.add({ name: "EV3Color"});

            var that = this;
            this.json_ajax_request('/brick_manager', 'get_bricks').success(
                function(response){
                    _.each(response.result, function(address, key, list){
                        that.add_to_selector(address);
                    });
                }) ;

        },
        events: {
            "submit #connect_form" : "subscribe_on_brick",
            "submit #add_brick" : "add_brick"

        },
        subscribe_on_brick: function(event){
            event.preventDefault();
            console.log("WOOO?");
        },
        add_brick: function(event){
            event.preventDefault();
            var that = this;
            var address = $('#address_input').val();
            this.json_ajax_request('/brick_manager', 'add_brick', address).success(
                function(response){
                    if (response.result == true){
                        that.add_to_selector(address);
                    }
                }
            )
        },
        add_to_selector : function(address){
            this.available_bricks.append(new Option(address, address));
        },

        render: function(){
            //view should be appended here
//            console.log(this.collection.models[0].toJSON());
//            var compiledTemplate = _.template( template, { sensors: this.collection.models } );
//            this.$el.html(compiledTemplate);
            return this; //Enable chained calls
        },

        json_ajax_request : function(object, method){
            var args = [].slice.apply(arguments);
            args = args.slice(2);

            var data = {
                'method' : method,
                'params' : args,
                'id' : 1
            };

             var request = {
                url: object,
                type: 'POST',
                contentType: "application/json",
                accepts: "application/json",
                cache: false,
                dataType: 'json',
                data: JSON.stringify(data)
            };
            return $.ajax(request);
        }

    });

    return AppView;
});


define([
    'jquery',
    'underscore',
    'backbone',
    'collections/sensor',
    'text!templates/app.html',
    'text!templates/header.html',
    'bootstrap'
], function($, _, Backbone, SensorCollection, template, HeaderTemplate){
    var AppView = Backbone.View.extend({
        el: '#app',

        header_template : _.template(HeaderTemplate),

        initialize: function () {
            this.$el.append(this.header_template); //render header

            this.available_bricks = $('#available_bricks');
            this.collection = new SensorCollection();
            this.collection.on('add', this.add_sensor, this);
            this.collection.on('change', this.add_sensor, this);

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
        add_sensor : function(sensor){
            console.log(sensor.toJSON().sample);
            this.$el.append(_.template(template)(sensor.toJSON()));
            console.log("new sensor added");
        },
        subscribe_on_brick: function(event){
            event.preventDefault();
            console.log("starting subscription");
            var address = this.available_bricks.find(':selected').text();
            this.collection.subscribe_on_brick(address);

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

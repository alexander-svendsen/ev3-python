define([
    'jquery',
    'underscore',
    'backbone',
    'collections/sensor',
    'views/sensorview',
    'text!templates/header.html',
    'text!templates/brick_controller.html',
    'bootstrap'
], function ($, _, Backbone, SensorCollection, SensorView, HeaderTemplate, BrickControllerTemplate) {
    var AppView = Backbone.View.extend({
        el: '#app',
        header_template: _.template(HeaderTemplate),
        initialize: function () {
            this.$el.prepend(this.header_template); //render header
            this.brick_info = $('#brick_info');
            this.old_address = '';

            this.available_bricks = $('#available_bricks');
            this.collection = new SensorCollection();
            this.collection.on('add', this.add_sensor, this);
//            this.collection.on('disconnect', this.diconnect, this);

            var that = this;
            this.json_ajax_request('/brick_manager', 'get_bricks').success(
                function (response) {
                    _.each(response.result, function (address, key, list) {
                        that.add_to_selector(address);
                    });
                });

        },
        events: {
            "submit #connect_form": "subscribe_on_brick",
            "submit #add_brick": "add_brick",
            "click #disconnect": "disconnect"
        },
        add_sensor: function (sensor) {
            var view = new SensorView({model: sensor});
            this.brick_info.append(view.render().el);
        },
        subscribe_on_brick: function (event) {
            event.preventDefault();
            var address = this.available_bricks.find(':selected').text();
            if (address != this.old_address) {
                this.old_address = address;
                this.brick_info.prepend(_.template(BrickControllerTemplate));
                this.collection.subscribe_on_brick(address);
            }
        },
        add_brick: function (event) {
            event.preventDefault();
            var that = this;
            var address = $('#address_input').val();
            this.json_ajax_request('/brick_manager', 'add_brick', address).success(
                function (response) {
                    if (response.result == true) {
                        that.add_to_selector(address);
                    }
                }
            )
        },
        add_to_selector: function (address) {
            this.available_bricks.append(new Option(address, address));
        },
        diconnect: function () {
            console.log("CALLLED DISCONNECT");
            this.collection.disconnect();
            return this;
        },
        json_ajax_request: function (object, method) {
            var args = [].slice.apply(arguments);
            args = args.slice(2);

            var data = {
                'method': method,
                'params': args,
                'id': 1
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

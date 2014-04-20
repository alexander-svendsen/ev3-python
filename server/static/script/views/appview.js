define([
    'jquery',
    'underscore',
    'views/baseview',
    'collections/sensor',
    'views/brickview',
    'views/sensorview',
    'text!templates/header.html',
    'bootstrap'
], function ($, _, BaseView, SensorCollection, BrickView, SensorView, HeaderTemplate) {
    var AppView = BaseView.extend({
        el: '#app',
        header_template: _.template(HeaderTemplate),
        initialize: function () {
            this.$el.prepend(this.header_template); //render header
            this.brick_info = $('#brick_info');
            this.old_address = '';

            this.available_bricks = $('#available_bricks');
            this.collection = new SensorCollection();
            this.collection.on('add', this.add_sensor, this);
            this.collection.on('serverDisconnected', this.disconnect, this);

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
            "submit #add_brick": "add_brick"
        },
        add_sensor: function (sensor) {
            var view = new SensorView({model: sensor});
            this.brick_info.append(view.render().el);
        },
        subscribe_on_brick: function (event) {
            event.preventDefault();
            var address = this.available_bricks.find(':selected').text();
            if (address != this.old_address) {
                if (this.old_address != ''){
                    this.close_socket();
                }

                this.old_address = address;
                this.brickView = new BrickView();
                this.brick_info.prepend(this.brickView.render().el);
                this.brickView.bind('disconnect', this.close_socket, this);

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
        close_socket: function (){
            this.old_address = '';
            this.collection.disconnect();
        },
        disconnect: function(){
            this.brickView.remove();
        }
    });

    return AppView;
});

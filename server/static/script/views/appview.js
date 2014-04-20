define([
    'jquery',
    'underscore',
    'views/baseview',
    'collections/sensor',
    'views/brickview',
    'views/sensorview',
    'text!templates/header.html',
    'bootstrap'  // to allow for the responsive design, we do not directly use it ourselves
], function ($, _, BaseView, SensorCollection, BrickView, SensorView, HeaderTemplate) {
    var AppView = BaseView.extend({
        el: '#app',
        headerTemplate: _.template(HeaderTemplate),

        initialize: function () {
            this.brickInfo = $('#brick');
            this.oldAddress = '';

            this.collection = new SensorCollection();
            this.collection.on('add', this.addSensor, this);
            this.collection.on('serverDisconnected', this.disconnect, this);

            var that = this;
            this.jsonRPC('/brick_manager', 'get_bricks').success(
                function (response) {
                    _.each(response.result, function (brickAddress) {
                        that.addToSelector(brickAddress);
                    });
                });

        },
        render: function(){
          this.$el.prepend(this.headerTemplate); //render header
          return this;
        },
        events: {
            "submit #connectForm": "connectToServer",
            "submit #addBrickForm": "addBrick"
        },
        addSensor: function (sensor) {
            var view = new SensorView({model: sensor});
            this.brickInfo.append(view.render().el);
        },
        connectToServer: function (event) {
            event.preventDefault();
            var address = $('#availableBricks').find(':selected').text();
            if (address != this.oldAddress) {
                if (this.oldAddress != '') {
                    this.closeConnection();
                }

                this.oldAddress = address;
                this.brickView = new BrickView();
                this.brickInfo.prepend(this.brickView.render().el);
                this.brickView.bind('close', this.closeConnection, this);

                this.collection.connectToServer(address);
            }
        },
        addBrick: function (event) {
            event.preventDefault();
            var that = this;
            var address = $('#address_input').val();
            this.jsonRPC('/brick_manager', 'add_brick', address).success(
                function (response) {
                    if (response.result == true) {
                        that.addToSelector(address);
                    }
                }
            )
        },
        addToSelector: function (address) {
            $('#availableBricks').append(new Option(address, address));
        },
        closeConnection: function () {
            this.oldAddress = '';
            this.collection.disconnect();
        },
        disconnect: function () {
            this.brickView.remove();
        }
    });

    return AppView;
});

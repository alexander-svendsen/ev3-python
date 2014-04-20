define([
    'jquery',
    'underscore',
    'views/baseview',
    'collections/sensor',
    'views/brickview',
    'views/sensorview',
    'views/alertview',
    'text!templates/header.html',
], function ($, _, BaseView, SensorCollection, BrickView, SensorView, AlertView, HeaderTemplate) {
    var AppView = BaseView.extend({
        el: '#app',
        headerTemplate: _.template(HeaderTemplate),

        initialize: function () {
            this.brickInfo = $('#brick');
            this.oldAddress = '';
            this.alertView = new AlertView();

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
        render: function () {
            this.$el.prepend(this.headerTemplate); //render header
            return this;
        },
        events: {
            "click #connectButton": "connectToServer",
            "click #addBrickButton": "addBrick"
        },
        addSensor: function (sensor) {
            var view = new SensorView({model: sensor});
            this.brickInfo.append(view.render().el);
        },
        connectToServer: function () {
            var address = $('#availableBricks').find(':selected').text();
            if (address != this.oldAddress) {
                if (this.oldAddress != '') {
                    this.closeConnection();
                }
                this.oldAddress = address;

                this.brickView = new BrickView();
                this.brickInfo.prepend(this.brickView.render().el);
                this.brickView.bind('close', this.closeConnection, this);

                this.$el.append(this.alertView.renderSuccess('Connected').el);
                this.collection.connectToServer(address);
            }
        },
        addBrick: function () {
            var that = this;
            var address = $('#addressInput').val();
            this.jsonRPC('/brick_manager', 'add_brick', address).success(
                function (response) {
                    if (response.result == true) {
                        that.addToSelector(address);
                        that.$el.append(this.alertView.renderSuccess('Brick added').el);
                    }
                })
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
            this.$el.append(this.alertView.renderError('Server got disconnected').el);
        }
    });

    return AppView;
});

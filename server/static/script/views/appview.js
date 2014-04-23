define([
    'jquery',
    'underscore',
    'views/baseview',
    'collections/sensor',
    'views/sensorview',
    'views/alertview',
    'views/codelistview',
    'bootstrap'
], function ($, _, BaseView, SensorCollection, SensorView, AlertView, CodeListView) {
    var AppView = BaseView.extend({
        el: '#app',
        connected: false,

        initialize: function () {
            this.brickInfo = $('#brick');
            this.alertView = new AlertView();

            this.collection = new SensorCollection();
            this.collection.on('add', this.addSensor, this);
            this.collection.on('serverDisconnected', this.disconnect, this);
            this.collection.on('onSocketOpen', this.renderConnectedProperly, this);

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
            "click #addBrickButton": "addBrick",
            "click #openSensorButton": "openSensor"
        },
        openSensor: function () {
            this.jsonRPC('/brick_manager', 'open_sensor',
                this.brickAddress, $('#sensorName').val().trim(), $('#portNumber').val().trim());
        },
        addSensor: function (sensor) {
            var view = new SensorView({model: sensor});
            this.brickInfo.append(view.render().el);
        },
        connectToServer: function () {
            var address = $('#availableBricks').find(':selected').text();

            if (this.connected) {
                this.collection.disconnect(true);
            }
            else{
                this.collection.connectToServer(address);
            }
        },
        renderConnectedProperly: function(){
            $('#connectButton').html('Disconnect!').addClass('btn-danger');
            $('#openSensorButton').removeClass('hide');
            this.codeView = new CodeListView();
            $(this.codeView.render().el).appendTo('#codeView');
            this.connected = true;
        },
        addBrick: function () {
            var that = this;
            var address = $('#addressInput').val().trim();
            this.jsonRPC('/brick_manager', 'add_brick', address).success(
                function (response) {
                    if (response.result == true) {
                        that.addToSelector(address);
                        that.$el.append(that.alertView.renderSuccess('Brick added').el);
                    }
                    else {
                        that.$el.append(that.alertView.renderError('No brick with that address found').el);
                    }
                })
        },
        addToSelector: function (address) {
            $('#availableBricks').append(new Option(address, address));
        },
        disconnect: function () {
            this.codeView.remove();
            $('#connectButton').html('Connect!').removeClass('btn-danger');
            $('#openSensorButton').addClass('hide');
            this.connected = false;
        }
    });
    return AppView;
});

define([
    'jquery',
    'underscore',
    'views/baseview',
    'views/alertview',
    'views/sensorlistview',
    'views/codelistview',
    'views/socketview',
    'bootstrap'
], function ($, _, BaseView, AlertView, SensorListView, CodeListView, SocketView) {
    var AppView = BaseView.extend({
        el: '#app',
        connected: false,

        initialize: function () {
            this.alertView = new AlertView();
            this.socket = new SocketView();

            this.socket.bind('onopen', this.onOpen, this);
            this.socket.bind('onclose', this.onClose, this);
            this.socket.bind('onmessage', this.onMessage, this);

            var that = this;
            this.jsonRPC('/brick_manager', 'get_bricks').success(
                function (response) {
                    _.each(response.result, function (brickAddress) {
                        that.addToSelector(brickAddress);
                    });
                });
        },
        events: {
            "click #connectButton": "connectOrDisconnect",
            "click #addBrickButton": "addBrick",
            "click #openSensorButton": "openSensor"
        },
        openSensor: function () {
            this.jsonRPC('/brick_manager', 'open_sensor',
                this.brickAddress, $('#sensorName').val().trim(), $('#portNumber').val().trim());
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
        connectOrDisconnect: function () {
            this.brickAddress = $('#availableBricks').find(':selected').text();
            if (this.connected) {
                this.socket.close();
            }
            else {
                this.socket.open();
            }
        },
        onMessage: function(message){
            var jsonData = $.parseJSON(message.data);
            this.sensorView.addMultiple(jsonData)
        },
        onOpen: function () {
            //Firstly send what brick we are interested in
            this.socket.send(this.brickAddress);

            //Fix the view
            $('#connectButton').html('Disconnect!').addClass('btn-danger').blur();
            $('#openSensorButton').removeClass('hide');

            this.sensorView = new SensorListView();
            this.codeView = new CodeListView();
            $(this.sensorView.render().el).appendTo('#brick');
            $(this.codeView.render().el).appendTo('#codeView');
            this.connected = true;
        },
        onClose: function () {
            this.codeView.close();
            this.sensorView.close();
            $('#connectButton').html('Connect!').removeClass('btn-danger').blur();
            $('#openSensorButton').addClass('hide');
            this.connected = false;
        }
    });
    return AppView;
});

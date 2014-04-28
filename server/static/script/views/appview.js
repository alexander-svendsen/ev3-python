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
            this.socket.bind('onclose', this.onUnexpectedClose, this);
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
            this.brickAddress = $('#availableBricks').get(0).value;
            if (this.connected) {
                this.socket.closeConnection(true);
                this.onClose();
            }
            else {
                this.socket.openConnection();
            }
        },
        onMessage: function (message) {
            var jsonData = $.parseJSON(message.data);
            if (jsonData['cmd'] == 'sensor_data') {
                this.sensorView.addMultiple(jsonData['data']);
            }
            else if (jsonData['cmd'] == 'code_data') {
                this.codeView.addMultiple(jsonData['data']);
            }
            else if (jsonData['cmd'] == 'remove_code') {
                this.codeView.removeOne(jsonData['title'])
            }
            else if(jsonData['cmd'] == 'running'){
                this.codeView.newRunning(jsonData['title']);
            }
            else {
                console.log("strange data");
            }
        },
        onOpen: function () {
            //Firstly send what brick we are interested in
            var data = {
                cmd: 'subscribe',
                brick_address: this.brickAddress
            };
            this.socket.send(JSON.stringify(data));

            //Fix the view
            $('#connectButton').html('Disconnect!').addClass('btn-danger').blur();
            $('#openSensorButton').removeClass('hide');

            this.sensorView = new SensorListView();
            this.codeView = new CodeListView({socket: this.socket});
            $(this.sensorView.render().el).appendTo('#brick');
            $(this.codeView.render().el).appendTo('#codeView');
            this.connected = true;
        },
        onUnexpectedClose: function () {
            this.$el.append(this.alertView.renderError("Can't connect to server").el);
            this.onClose();
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

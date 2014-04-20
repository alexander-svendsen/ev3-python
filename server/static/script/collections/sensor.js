define([
    'underscore',
    'backbone',
    'models/sensor'
], function (_, Backbone, SensorModel) {
    var SensorCollection = Backbone.Collection.extend({
        model: SensorModel,
        socket: null,
        closedFromServer: false,  //to avoid a round dependency

        setCollection: function (sensors) {
            var that = this;
            _.each(sensors, function (sensor) {
                that.add(sensor);
            });
        },
        connectToServer: function (brick_address) {
            if (!this.socket) {
                this.initializeWebSocket("ws://127.0.1.1:9999/");
            }
            if (this.socket.readyState == 1) {
                this.socket.send(brick_address);
            } else {
                var that = this;
                this.socket.onopen = function () {
                    that.socket.send(brick_address);
                };
            }

        },
        initializeWebSocket: function (address) {
            var that = this;
            this.socket = new WebSocket(address);
            this.socket.onmessage = function (msg) {
                var jsonData = $.parseJSON(msg.data);
                that.setCollection(jsonData);
            };
            this.socket.onclose = function () {
                console.log("Socket.close");
                that.disconnect();
                if (that.closedFromServer){
                    that.closedFromServer = false;
                }else{
                    that.trigger('serverDisconnected');
                }
            };

        },
        disconnect: function (silent) {
           if (silent){
                this.closedFromServer = true;
            }

            if (this.socket){
                this.socket.close();
                this.socket = null;
            }

            this.clear(); //cannot use reset as it does not trigger any model event
        },
        add: function (sensor) {
            if (sensor == undefined) {
                return;
            }

            var newSensor = new SensorModel(sensor);
            var duplicate = this.find(function (model) {
                return model.eql(newSensor);
            });
            if (duplicate) {
                duplicate.set(newSensor.toJSON());
            }
            else {
                Backbone.Collection.prototype.add.call(this, newSensor);
            }
        },
        clear: function () {
           var that = this;
            _.each(this.models, function(model) {
                that._removeReference(model);
                model.trigger('remove', model, that);
            });
            this._reset();
        }
    });
    return SensorCollection;
});
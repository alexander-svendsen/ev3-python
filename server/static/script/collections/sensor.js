define([
    'underscore',
    'backbone',
    'models/sensor'
], function (_, Backbone, SensorModel) {
    var SensorCollection = Backbone.Collection.extend({
        model: SensorModel,
        socket: null,
        set_sensor_collection: function (sensor_list) {
            var that = this;
            _.each(sensor_list, function (sensor) {
                that.add(sensor);
            });
        },
        subscribe_on_brick: function (brick_address) {
            if (!this.socket) {
                this.initialize_websocket("ws://127.0.1.1:9999/");
            }
            var that = this;
            if (this.socket.readyState == 1) {
                this.socket.send(brick_address);
            } else {
                this.socket.onopen = function () {
                    that.socket.send(brick_address);
                }
            }

        },
        initialize_websocket: function (address) {
            var that = this;
            this.socket = new WebSocket(address);
            this.socket.onmessage = function (msg) {
                var json_data = $.parseJSON(msg.data);
                that.set_sensor_collection(json_data);
            };
            this.socket.onclose = function (msg) {
                console.log("Socket.close");
                that.disconnect();
                that.trigger('serverDisconnected');
            };
        },
        disconnect: function () {
            console.log("disconnected socket");
            if (this.socket){
                this.socket.close();
                this.socket = null;
            }
            this.clear(); //cannot use reset as it does not trigger any model event
        },
        add: function (sensor_data) {
            if (sensor_data == undefined) {
                return;
            }

            var new_sensor = new SensorModel(sensor_data);
            var duplicate = this.find(function (model) {
                return model.eql(new_sensor);
            });
            if (duplicate) {
                duplicate.set(new_sensor.toJSON());
            }
            else {
                Backbone.Collection.prototype.add.call(this, new_sensor);
            }
        },
        clear: function () {
           var that = this;
            _.each(this.models, function(model) {
                that._removeReference(model);
                model.trigger('remove', model, that);
            });
            this._reset();
            return this;
        }
    });
    return SensorCollection;
});
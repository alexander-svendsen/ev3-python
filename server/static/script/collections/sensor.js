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
            _.each(sensor_list, function(sensor, key, list){
                that.add(sensor);
            });
        },
        subscribe_on_brick: function (brick_address) {
            if (!this.socket){
                this.initialize_websocket("ws://127.0.1.1:9999/");
            }
            var that = this;
            if (this.socket.readyState == 1){
                this.socket.send(brick_address);
            }else{
                this.socket.onopen = function(){
                    that.socket.send(brick_address);
                }
            }

        },
        initialize_websocket: function (address) {
            var that = this;
            this.socket = new WebSocket(address);
            this.socket.onopen = function () {
                console.log("Socket has been opened!");
            };
            this.socket.onmessage = function (msg) {
                var json_data = $.parseJSON(msg.data);
                that.set_sensor_collection(json_data);
            };
            this.socket.onerror = function (msg) {
                console.log("socket got an error, it got closed");
                that.disconnect();
            };
            this.socket.onclose = function (msg) {
                console.log("closed the socket");
                that.disconnect();
            };
        },
        disconnect: function(){
            this.trigger('disconnect');
            this.reset();
            this.socket = null;
        },
        add: function (sensor_data) {
            var new_sensor = new SensorModel(sensor_data);
            var duplicate = this.find(function (model) {
                return model.eql(new_sensor);
            });
            if (duplicate){
                console.log("updated old");
                duplicate.set(new_sensor.toJSON());
            }
            else{
                console.log("saving new sensor");
                Backbone.Collection.prototype.add.call(this, new_sensor);
            }
        }
    });
    return SensorCollection;
});
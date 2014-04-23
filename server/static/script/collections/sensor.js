define([
    'underscore',
    'backbone',
    'models/sensor'
], function (_, Backbone, SensorModel) {
    var SensorCollection = Backbone.Collection.extend({
        model: SensorModel,
        socket: null,
        brickAddress: '',

        setCollection: function (sensors) {
            var that = this;
            _.each(sensors, function (sensor) {
                that.add(sensor);
            });
        },
        connectToServer: function (brickAddress) {
            this.brickAddress = brickAddress;
            if (!this.socket) {
                this.initializeWebSocket("ws://127.0.1.1:9999/");
            }
        },
        onSocketOpen :function(){
            this.trigger('onSocketOpen');
            this.socket.send(this.brickAddress);
        },
        initializeWebSocket: function (address) {
            var that = this;
            this.socket = new WebSocket(address);
            this.socket.onmessage = function (msg) {
                var jsonData = $.parseJSON(msg.data);
                that.setCollection(jsonData);
            };
            this.socket.onclose = function () {
                that.disconnect();
                that.trigger('serverDisconnected');
            };
            this.socket.onopen = function () {
                that.onSocketOpen();
            };
        },
        disconnect: function () {
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
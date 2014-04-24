define([
    'underscore',
    'backbone',
    'models/sensor'
], function (_, Backbone, SensorModel) {
    var SensorCollection = Backbone.Collection.extend({
        model: SensorModel,
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
            _.each(this.models, function (model) {
                that._removeReference(model);
                model.trigger('remove', model, that);
            });
            this._reset();
        }
    });
    return SensorCollection;
});
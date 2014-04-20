define([
    'underscore',
    'backbone'
], function (_, Backbone) {
    var SensorModel = Backbone.Model.extend({
        defaults: {
            port: 0,
            name: "Sensor",
            mode: "Mode",
            sample: [0.0]
        },
        eql: function (other) {
            return this.get('port') == other.get('port');
        }
    });
    return SensorModel;
});
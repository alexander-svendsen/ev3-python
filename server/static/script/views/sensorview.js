define([
    'jquery',
    'underscore',
    'backbone',
    'text!templates/sensor.html'
], function ($, _, Backbone, SensorTemplate) {
    var SensorView = Backbone.View.extend({
        template: _.template(SensorTemplate),
        initialize: function () {
            this.model.on('change', this.render, this);
            this.model.on('destroy', this.remove, this);
        },
        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }
    });
    return SensorView;
});
define([
    'jquery',
    'underscore',
    'views/baseview',
    'text!templates/sensor.html'
], function ($, _, BaseView, Template) {
    var SensorView = BaseView.extend({
        template: _.template(Template),
        initialize: function () {
            this.model.on('change', this.render, this);
            this.model.on('remove', this.remove, this);
        },
        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }
    });
    return SensorView;
});
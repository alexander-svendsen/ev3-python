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
            this.model.on('destroy', this.close, this);
        },
        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        },
        close: function () {
            this.unbind();
            this.model.unbind('change', this.render, this);
            this.model.unbind('destroy', this.close, this);
            this.remove();
            delete this.$el;
            delete this.el;
        }
    });
    return SensorView;
});
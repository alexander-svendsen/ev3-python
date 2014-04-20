define([
    'jquery',
    'underscore',
    'views/baseview',
    'text!templates/brick.html'
], function ($, _, BaseView, Template) {
    var BrickView = BaseView.extend({
        template: _.template(Template),

        render: function () {
            this.$el.html(this.template);
            return this;
        },
        events: {
            "click #closeBrickButton": "close",
            "click #openSensorButton": "openSensor"
        },
        close: function () {
            this.trigger('close');
            this.remove();
        },
        openSensor: function () {
            console.log("mordi");
        }
    });
    return BrickView;
});
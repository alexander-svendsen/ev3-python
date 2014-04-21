define([
    'jquery',
    'underscore',
    'views/baseview',
    'text!templates/brick.html',
    'bootstrap'
], function ($, _, BaseView, Template) {
    var BrickView = BaseView.extend({
        template: _.template(Template),

        initialize: function (option) {
            this.alertView = option.alertView;
            this.brickAddress = option.brickAddress;
        },
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
            this.jsonRPC('/brick_manager', 'open_sensor', this.brickAddress, $('#sensorName').val(), $('#portNumber').val());

        }
    });
    return BrickView;
});
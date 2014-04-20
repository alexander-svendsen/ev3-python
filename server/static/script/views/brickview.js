define([
    'jquery',
    'underscore',
    'views/baseview',
    'text!templates/brick_controller.html'
], function ($, _, BaseView, Template) {
    var BrickView = BaseView.extend({
        template: _.template(Template),

        render: function () {
            this.$el.html(this.template);
            return this;
        },
        events: {
            "click #disconnect": "disconnect",
            "click #new_sensor": "new_sensor"
        },
        disconnect: function () {
            this.trigger('disconnect');
            this.remove();
        },
        new_sensor: function () {
            console.log("mordi");
        }
    });
    return BrickView;
});
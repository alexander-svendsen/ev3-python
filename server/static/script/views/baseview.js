define([
    'jquery',
    'underscore',
    'backbone'
], function ($, _, Backbone) {
    var BaseView = Backbone.View.extend({
        jsonRPC: function (object, method) {
            var args = [].slice.apply(arguments);
            args = args.slice(2);

            var data = {
                'method': method,
                'params': args,
                'id': 1
            };

            var request = {
                url: object,
                type: 'POST',
                contentType: "application/json",
                accepts: "application/json",
                cache: false,
                dataType: 'json',
                data: JSON.stringify(data)
            };
            return $.ajax(request);
        },
        close: function () {
            this.unbind();
            //should remove every bind here, as it will lead to zombie views

            this.remove();
            delete this.$el;
            delete this.el;
        }
    });
    return BaseView;
});
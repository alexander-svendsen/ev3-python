define([
    'jquery',
    'underscore',
    'backbone'
], function ($, _, Backbone) {
    var BaseView = Backbone.View.extend({
        json_ajax_request: function (object, method) {
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
        }
    });
    return BaseView;
});
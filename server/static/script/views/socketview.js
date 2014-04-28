define([
    'jquery',
    'underscore',
    'backbone'
], function ($, _, Backbone) {
    //Controller for handling socket communication and event propagation based on it
    var SocketView = Backbone.View.extend({
        initialize: function () {
            this.silent = false;
        },
        send: function (msg) {
            this.socket.send(msg);
        },
        onopen: function () {
            this.trigger('onopen');
        },
        onclose: function () {
            if (!this.silent) {
                this.trigger('onclose');
                this.silent = false;
            }
        },
        onerror: function () {
            this.trigger('onerror');
        },
        onmessage: function (message) {
            this.trigger('onmessage', message);
        },
        openConnection: function () {
            var that = this;
            this.socket = new WebSocket('ws://'+ window.location.hostname +':9999/');
            this.socket.onmessage = function(message){that.onmessage(message)};
            this.socket.onclose = function(){that.onclose()};
            this.socket.onopen = function(){that.onopen()};
            this.socket.onerror = function(){that.onerror()};
        },
        closeConnection: function (silent) {
            this.silent = silent;
            this.socket.close();
        }
    });

    return SocketView;
});

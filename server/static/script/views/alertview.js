define([
    'jquery',
    'underscore',
    'backbone',
    'text!templates/alert.html'
], function ($, _, Backbone, Template) {
    var AlertView = Backbone.View.extend({
        template: _.template(Template),
        timeOutPointer: null,
        events: {
          "click .close" : "clear"
        },
        clear: function (){
            clearTimeout(this.timeOutPointer);
            this.$el.html('');
        },
        clearViewTimer: function(time){
            clearTimeout(this.timeOutPointer);
            var that = this;
            this.timeOutPointer = setTimeout(function(){
                that.$el.html('');
            },time);
        },
        renderWarning: function(msg){
            return this.render({msg: msg, alertType: 'alert-warning'});
        },
        renderError: function(msg){
            return this.render({msg: msg, alertType: 'alert-danger'})
        },
        renderSuccess: function(msg){
            return this.render({msg: msg, alertType: 'alert-success'})
        },
        render: function (dict) {
            this.$el.html(this.template(dict));
            this.clearViewTimer(3000);
            return this;
        }
    });
    return AlertView;
});
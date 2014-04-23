define([
    'underscore',
    'backbone'
], function (_, Backbone) {
    var CodeModel = Backbone.Model.extend({
        defaults: {
            title: '',
            code: '',
            running: false
        }
    });
    return CodeModel
});

define([
    'underscore',
    'backbone'
], function (_, Backbone) {
    var CodeModel = Backbone.Model.extend({
        defaults: {
            title: '',
            code: '',
            running: false
        },
        eql: function (other) {
            return this.get('title') == other.get('title');
        }
    });
    return CodeModel
});

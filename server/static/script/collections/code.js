define([
    'underscore',
    'backbone',
    'models/code'
], function (_, Backbone, CodeModel) {
     var CodeCollection = Backbone.Collection.extend({
        model: CodeModel
     });
    return CodeCollection;
});

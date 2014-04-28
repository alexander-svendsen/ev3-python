define([
    'underscore',
    'backbone',
    'models/code'
], function (_, Backbone, CodeModel) {
     var CodeCollection = Backbone.Collection.extend({
        model: CodeModel,
        add: function (code) {
            if (code == undefined) {
                return;
            }
            var newCodeModel = new CodeModel(code);
            var duplicate = this.find(function (model) {
                return model.eql(newCodeModel);
            });
            if (duplicate) {
                duplicate.set(newCodeModel.toJSON());
                return duplicate;
            }
            else {
                return Backbone.Collection.prototype.add.call(this, newCodeModel);
            }
        },
        clear: function () {
            var that = this;
            _.each(this.models, function (model) {
                that._removeReference(model);
                model.trigger('remove', model, that);
            });
            this._reset();
        }
     });
    return CodeCollection;
});

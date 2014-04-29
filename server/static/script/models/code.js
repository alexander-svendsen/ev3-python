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
        changed : null,
        getChanged: function(){
            var temp = this.changed;
            this.changed = false;
            return temp;
        },
        set: function(attributes, options) {
            if (attributes.code){
                this.changed = attributes.code != this.get('code');
            }

            return Backbone.Model.prototype.set.call(this, attributes, options);
        },
        eql: function (other) {
            return this.get('title') == other.get('title');
        }
    });
    return CodeModel
});

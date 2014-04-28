define([
    'jquery',
    'underscore',
    'views/baseview',
    'text!templates/code.html'
], function ($, _, BaseView, Template) {
    var CodeView = BaseView.extend({
        tagName: 'a',
        template: _.template(Template),

        initialize: function (option) {
            this.selected = false;
            this.model.on('change', this.render, this);
            this.model.on('destroy', this.close, this);
            this.model.on('select', this.viewCode, this);
            this.codeMirror = option.codeMirror;
        },

        render: function () {
            this.$el.addClass('list-group-item');
            if (this.model.get('running')) {
                this.$el.addClass('list-group-item-success')
            } else {
                this.$el.removeClass('list-group-item-success')
            }
            this.$el.html(this.template(this.model.toJSON()));
            if (this.selected) {
                this.setCodeInCodeMirror();
            }
            return this;
        },
        events: {
            'click': 'viewCode',
            'click .close': 'removeCodeModule'
        },
        viewCode: function () {
            this.selected = true;
            this.trigger('selected', this);
            this.setCodeInCodeMirror();
        },
        setCodeInCodeMirror: function () {
            this.codeMirror.setValue(this.model.get('code'));
        },
        removeCodeModule: function () {
            this.model.destroy();
        },
        activateView: function () {
            this.$el.addClass('active');
        },
        deactivateView: function () {
            if (this.$el) { //just in case it got removed
                this.$el.removeClass('active')
            }
        },
        close: function () {  //removes the zombies
            this.unbind();
            this.model.unbind('change', this.render, this);
            this.model.unbind('destroy', this.close, this);
            this.model.unbind('select', this.viewCode, this);
            this.remove();
            delete this.$el;
            delete this.el;
        }
    });
    return CodeView
});
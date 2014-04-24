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
            this.model.on('change', this.render, this);
            this.model.on('destroy', this.close, this);
            this.codeMirror = option.codeMirror;
        },

        render: function () {
            this.$el.addClass('list-group-item');
            if (this.model.get('running')){
                this.$el.addClass('list-group-item-success')
            }else{
                this.$el.removeClass('list-group-item-success')
            }
            this.$el.html(this.template(this.model.toJSON()));
            this.input = this.$('.edit');
            return this;
        },
        events: {
            'click' : 'viewCode',
            'dblclick': 'editTitle',
            'blur .edit': 'closeEditOnTitle',
            'click .close': 'removeCodeModule',
            'keypress .edit': 'closeEditOnTitleOnKeyPress'
        },
        viewCode: function(){
            this.trigger('selected', this);
            this.codeMirror.setValue(this.model.get('code'));
        },
        editTitle: function () {
            this.$el.addClass('editing');
            this.input.focus();
        },
        closeEditOnTitle: function () {
            var value = this.input.val().trim();
            if (value) {
                this.model.set({title: value});
            }
            this.$el.removeClass('editing');
        },
        closeEditOnTitleOnKeyPress: function(event){
            if (event.keyCode == 13){
                this.closeEditOnTitle();
            }
        },
        removeCodeModule: function () {
            this.model.destroy();
        },
        activateView: function(){
            this.$el.addClass('active');
        },
        deactivateView: function(){
            if (this.$el){ //just in case it got removed
                this.$el.removeClass('active')
            }
        },
        close: function () {  //removes the zombies
            this.unbind();
            this.model.unbind('change', this.render, this);
            this.model.unbind('destroy', this.close, this);
            this.remove();
            delete this.$el;
            delete this.el;
        }
    });
    return CodeView
});
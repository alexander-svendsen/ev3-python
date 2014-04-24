define([
    'jquery',
    'underscore',
    'views/baseview',
    'views/codeview',
    'collections/code',
    'text!templates/codelist.html',
    'libs/codemirror/codemirror',
    'libs/codemirror/mode/python/python'
], function ($, _, BaseView, CodeView, CodeCollection, Template, CodeMirror) {
    var CodeListView = BaseView.extend({
        collection: new CodeCollection(),
        template: _.template(Template),
        selectedView: null,

        initialize: function () {
            this.collection.on('add', this.add, this);
            this.collection.on('reset', this.reset, this);
            this.collection.on('remove', this.fixProperViewAfterRemove, this);
        },
        render: function () {
            this.$el.html(this.template);
            this.codeMirror = this.createEditor();
            this.input = this.$('#newModule');
            return this;
        },
        events: {
            'submit form': 'createCodeSnippet',
            'click #save': 'saveCodeToModule'
        },
        saveCodeToModule: function () {
            if (this.selectedView) {
                this.selectedView.model.set({code: this.codeMirror.getValue()})
            }
        },
        createCodeSnippet: function (event) {
            event.preventDefault();
            var title = this.input.val().trim();
            if (!title) {
                return;
            }
            var data = {
                title: this.input.val().trim(),
                running: false,
                code: '\nclass SomeBehaviorName(Behavior):' +
                    '\n\tdef check(self):' +
                    '\n\t\tpass' +
                    '\n\tdef action(self):' +
                    '\n\t\tpass' +
                    '\n\tdef suppress(self):' +
                    '\n\t\tpass'
            };

            this.collection.add(data);
            this.input.val('');
        },
        add: function (codeModule) {
            var view = new CodeView({model: codeModule, codeMirror: this.codeMirror});
            $('#codeList').append(view.render().el);
            $('#editorWithButtons').removeClass('hide');
            view.bind('selected', this.switchSelectedView, this);
            view.viewCode();
        },
        switchSelectedView: function (view) {
            if (this.selectedView) {
                this.selectedView.deactivateView();
                this.saveCodeToModule();
            }
            this.selectedView = view;
            this.selectedView.activateView();
        },
        reset: function () {
            $('#codeList').html('');
            this.collection.each(this.add(), this);
        },
        createEditor: function () {
            var that = this;
            var codeMirror = CodeMirror(function (el) {
                that.$('#codeWindow').html(el);

            }, {
                lineNumbers: true,
                mode: {name: "python",
                    version: 2,
                    singleLineStringErrors: false},
                value: '# Code should go here \n',
                indentUnit: 4,
                matchBrackets: true
            });

            CodeMirror.commands.save = function () {
                that.saveCodeToModule()
            };
            return codeMirror
        },
        fixProperViewAfterRemove: function (model) {
            if (this.collection.length == 0) {
                $('#editorWithButtons').addClass('hide');
                return;
            }

            if (this.selectedView.model == model) {
                this.codeMirror.setValue('# code should go here');
            }
        },
        close: function () {

            this.unbind();
            this.collection.unbind('add', this.add, this);
            this.collection.unbind('reset', this.reset, this);
            this.collection.unbind('remove', this.fixProperViewAfterRemove, this);

            this.remove();
            delete this.$el; // Delete the jQuery wrapped object variable
            delete this.el; // Delete the variable reference to this node
        }

    });
    return CodeListView
});

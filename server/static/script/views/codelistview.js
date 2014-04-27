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
        template: _.template(Template),
        selectedView: null,

        initialize: function (option) {
            this.collection = new CodeCollection();
            this.collection.on('add', this.add, this);
            this.collection.on('reset', this.reset, this);
            this.collection.on('remove', this.fixProperViewAfterRemove, this);
            this.socket = option.socket
        },
        render: function () {
            this.$el.html(this.template);
            this.codeMirror = this.createEditor();
            this.input = this.$('#newModule');
            return this;
        },
        events: {
            'submit form': 'createCodeSnippet',
            'click #save': 'saveCodeToModule',
            'click #run': 'runCode',
            'click #stop': 'stopCode',
            'click #pause': 'pauseCode'
        },
        runCode: function () {
            //TODO
        },
        stopCode: function () {
            //TODO
        },
        pauseCode: function () {
            //TODO
        },
        saveCodeToModule: function () {
            if (this.selectedView) {
                this.saveCodeInView();
                var data = this.selectedView.model.toJSON();
                data['cmd'] = 'code';
                this.socket.send(JSON.stringify(data));
            }
        },
        saveCodeInView: function () {
            this.selectedView.model.set({code: this.codeMirror.getValue()});
        },
        createCodeSnippet: function (event) {
            event.preventDefault();
            var title = this.input.val().trim();
            if (!title) {
                return;
            }
            var duplicate = this.collection.findWhere({title: title});
            if (duplicate) {
                duplicate.trigger('select');
                return
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
            this.$('#codeList').append(view.render().el);
            this.$('#editorWithButtons').removeClass('hide');
            view.bind('selected', this.switchSelectedView, this);
            view.viewCode();
        },
        addMultiple: function (codeList) {
            var that = this;
            _.each(codeList, function (code) {
                that.collection.add(code);
            });
        },
        switchSelectedView: function (view) {
            if (this.selectedView) {
                this.selectedView.deactivateView();
                this.saveCodeInView()
            }
            this.selectedView = view;
            this.selectedView.activateView();
        },
        reset: function () {
            this.$('#codeList').html('');
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
                this.$('#editorWithButtons').addClass('hide');
            }
            else if (this.selectedView.model == model) {
                this.collection.models[0].trigger('select');
            }
            var data = {title: model.toJSON().title, cmd: 'remove_code'};
            console.log(this.collection);
            this.socket.send(JSON.stringify(data));
        },
        close: function () {

            this.unbind();
            this.collection.unbind('add', this.add, this);
            this.collection.unbind('reset', this.reset, this);
            this.collection.unbind('remove', this.fixProperViewAfterRemove, this);

            this.remove();
            delete this.$el;
            delete this.el;
        }

    });
    return CodeListView
});

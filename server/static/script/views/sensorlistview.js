define([
    'jquery',
    'underscore',
    'views/baseview',
    'views/sensorview',
    'collections/sensor'
], function ($, _, BaseView, SensorView, SensorCollection) {
    var SensorListView = BaseView.extend({
        collection: new SensorCollection(),
        initialize: function () {
            this.collection.on('add', this.add, this);
        },
        add: function (sensor) {
            var view = new SensorView({model: sensor});
            this.$el.append(view.render().el);
        },
        addMultiple: function (sensors) {
            var that = this;
            _.each(sensors, function (sensor) {
                that.collection.add(sensor);
            });
        },
        close: function () {
            this.unbind();
            this.collection.unbind('add', this.add, this);
            this.collection.clear();

            this.remove();
            delete this.$el;
            delete this.el;
        }
    });
    return SensorListView;
});

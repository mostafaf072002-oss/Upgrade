odoo.define("Real_Estate.property_dashboard", function (require) {
    "use strict";

    var AbstractAction = require("web.AbstractAction");
    var core = require("web.core");

    var PropertyDashboard = AbstractAction.extend({
        template: "property_dashboard",

        init: function (parent, action) {
            this._super(parent, action);
            this.properties = [];
        },

        // دالة جلب البيانات
        _loadProperties: function () {
            var self = this;

            return this._rpc({
                model: "real.estate.property",
                method: "search_read",
                args: [[], [
                    "name",
                    "code",
                    "expected_price",
                    "selling_price",
                    "state"
                ]],
            }).then(function (result) {
                self.properties = result;
            });
        },

        willStart: function () {
            return Promise.all([
                this._super.apply(this, arguments),
                this._loadProperties(),
            ]);
        },

        start: function () {
            console.log(this.properties);
            return this._super();
        },
    });

    core.action_registry.add(
        "real_estate_property_dashboard",
        PropertyDashboard
    );

    return PropertyDashboard;
});
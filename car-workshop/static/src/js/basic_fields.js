odoo.define('car-workshop.basic_fields', function (require) {
    "use_strict";



    var fields = require('web.basic_fields');

    fields.InputField.include({
        _prepareInput: function ($input) {
            this.$input = this._super.apply(this, arguments);
            this.isMobile= function() {
                try {
                    document.createEvent('TouchEvent');
                    return true;
                } catch (ex) {
                    return false;
                }
            };
            if (this.attrs.options && this.attrs.options.hasOwnProperty("input_type") && this.isMobile()) {
                this.$input.attr({
                    type: this.attrs.options.input_type
                });
                return this.$input;
            };
        }
    });
});

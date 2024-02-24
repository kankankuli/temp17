odoo.define('pos_add_product_barcode_no_reload.ProductScreen', function (require) {
    'use strict';

    var screens = require('point_of_sale.screens');
    var ProductScreenWidget = screens.ProductScreenWidget;

    ProductScreenWidget.include({
        barcode_product_action: async function(code){
            var self = this;
            const res = await this.pos.check_product_barcode(code);
             if (res) {
                 if (self.pos.scan_product(code)) {
                    if (self.barcode_product_screen) {
                        self.gui.show_screen(self.barcode_product_screen, null, null, true);
                    }
                 } else {
                    this.barcode_error_action(code);
                 }
             }
             else{
                this.barcode_error_action(code);
             }
        },
    });
});

/** @odoo-module */
import { _t } from "@web/core/l10n/translation";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { useService } from "@web/core/utils/hooks";
import { PosCalculatorPopup } from "@wbl_calculator_in_pos/app/pos_calculator_popup/PosCalculatorPopup";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { Component } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";


export class PosCalculator extends Component {
    static template = "wbl_calculator_in_pos.PosCalculator";
    setup() {
        this.pos = usePos();
        this.popup = useService("popup");
    }
    async click() {
        var self = this;
        const { confirmed, payload } = await this.popup.add(PosCalculatorPopup, {
            title: _t("Calculator"),
        });
    }
}
ProductScreen.addControlButton({
    component: PosCalculator,
    condition: function () {
        return true;
    },
});

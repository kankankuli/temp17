/** @odoo-module */

import { _t } from "@web/core/l10n/translation";
import { AbstractAwaitablePopup } from "@point_of_sale/app/popup/abstract_awaitable_popup";
import { useService } from "@web/core/utils/hooks";
import { useState, useRef, onMounted } from "@odoo/owl";

export class PosCalculatorPopup extends AbstractAwaitablePopup {
    static template = "wbl_calculator_in_pos.PosCalculatorPopup";

    setup() {
        super.setup();
        this.currentInput = '';
        this.currentOperator = '';
        this.result = 0;
        this.keyboardNumbers = {
            '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
            '7': 7, '8': 8, '9': 9, '0': 0, '.': '.'
        };
        this.keyboardOperators = {
            '+': '+',
            '-': '-',
            '*': '*',
            '/': '/',
            '%': '%'
        };
        window.addEventListener("keydown", this._onKeyDown.bind(this));
    }
    _onKeyDown(event) {
        if (event.key in this.keyboardNumbers) {
            if (event.key === '.') {
	            if (this.currentInput.indexOf('.') === -1) {
                    this.currentInput += event.key;
                    $("#result").html(this.currentInput);
                }
            } else {
	            this.currentInput += event.key;
	            $("#result").html(this.currentInput);
	        }
        }
        if (event.key in this.keyboardOperators) {
            if (this.currentInput !== '') {
	            if (this.currentOperator !== '') {
	                this.result = this.calculate(this.result, parseFloat(this.currentInput), this.currentOperator);
	                $("#result").html(this.result);
	            }
	            else {
	                this.result = parseFloat(this.currentInput);
	            }
	            this.currentInput = '';
	            this.currentOperator = event.key;
            }
        }
        if (event.key === 'Backspace') {
            this.currentInput = this.currentInput.substring(0, this.currentInput.length - 1);
            $("#result").html(this.currentInput);
        }
        if (event.key === 'Enter') {
			if (this.currentInput !== '') {
	            this.result = this.calculate(this.result, parseFloat(this.currentInput), this.currentOperator);
	            $("#result").html(this.result);
	            this.currentInput = this.result.toString();
	            this.currentOperator = '';
	        }
        }
    }
    sendNumberInput(event) {
        var $input = $(event.currentTarget);
	    var numberKey = $input.attr('data-key');
	    if (numberKey === '.') {
            this.sendDecimalInput(event);
        }
        else {
            this.currentInput += numberKey;
            $("#result").html(this.currentInput);
        }
    }
    clearInputBuffer(event) {
        var $input = $(event.currentTarget);
	    var cleanKey = $input.attr('data-key');
	    this.result = 0;
        this.currentInput = '';
        this.currentOperator = '';
	    $("#result").html('');
	    $("#expression").html('');
    }
    calculateOperator(event) {
        var $input = $(event.currentTarget);
	    var operatorKey = $input.attr('data-key');
	    if (this.currentInput !== '') {
            if (this.currentOperator !== '') {
                this.result = this.calculate(this.result, parseFloat(this.currentInput), this.currentOperator);
                $("#result").html(this.result);
            }
            else {
                this.result = parseFloat(this.currentInput);
            }
            this.currentInput = '';
            this.currentOperator = operatorKey;
        }
    }
    calculateEqualOperator(event) {
        var $input = $(event.currentTarget);
	    var equalKey = $input.attr('data-key');
	    if (this.currentInput !== '') {
            this.result = this.calculate(this.result, parseFloat(this.currentInput), this.currentOperator);
            $("#result").html(this.result);
            this.currentInput = this.result.toString();
            this.currentOperator = '';
        }
    }
    sendDecimalInput(event) {
        var $input = $(event.currentTarget);
	    var decimalKey = $input.attr('data-key');
        if (this.currentInput.indexOf('.') === -1) {
            this.currentInput += decimalKey;
            $("#result").html(this.currentInput);
        }
    }
    sendBackspace(event) {
        var $input = $(event.currentTarget);
	    var backspaceKey = $input.attr('data-key');
	    this.currentInput = this.currentInput.substring(0, this.currentInput.length - 1);
        $("#result").html(this.currentInput);
    }
    calculate(number1, number2, operator) {
        $("#expression").html(number1 + operator + number2);
        switch (operator) {
            case '+':
                return number1 + number2;
            case '-':
                return number1 - number2;
            case '*':
                return number1 * number2;
            case '/':
                return number1 / number2;
            case '%':
                return (number1 / 100) * number2;
            default:
                return number2;
        }
    }
}

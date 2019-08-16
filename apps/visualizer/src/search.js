import Vue from 'vue';

const request = require('request');

Vue.component('stock-search', {
    data: function() {
        return {
            symbol: '',
            displayElements: [],
            showDropdown: false,
            selectedOption: 0
        }
    },
    methods: {
        selectStock(symbol, name) {
            this.$store.commit('addStock', {symbol, name});
            this.$data.showDropdown = false;
            this.$data.selectedOption = 0;
            this.$refs.stockInput.value = "";
        },
        onKeydown(e) {
            if (e.defaultPrevented) {
                return;
            }

            if (e.key == "Enter") {
                let stk = this.$data.displayElements[this.$data.selectedOption]
                this.selectStock(stk.symbol, stk.name);
                e.preventDefault();
                return;
            }

            const isUp = (e.key == "ArrowUp");
            const isDown = (e.key == "ArrowDown");
            
            if (!isUp && !isDown) {
                return;
            }

            const dir = isDown ? 1 : -1;
            this.$data.selectedOption += dir;
            e.preventDefault();
        },
        onInput(e) {
            if (e.target.value == this.$data.symbol) {
                return;
            }

            this.$data.symbol = e.target.value;

            // Perform stock search
            request({
                uri: 'http://127.0.0.1:5000/search',
                qs: {
                    'inp': this.$data.symbol
                }
            }, (err, response, body) => {
                this.$data.displayElements = JSON.parse(body);
                this.showUpdateSearchDropdown();
            });
        },
        showUpdateSearchDropdown() {
            this.$data.showDropdown = !!this.$data.symbol;
            this.$data.selectedOption = Math.min(
                Math.max(
                    this.$data.selectedOption,
                    0),
                this.$data.displayElements.length - 1);
        },
    },
    template: `
        <div class="dropdown" v-bind:class="{'is-active': showDropdown}">
            <p class="control has-icons-left">
                <input ref="stockInput"
                       class="input is-rounded"
                       type="text"
                       placeholder="GOOG"
                       v-on:input="onInput($event)"
                       v-on:keydown="onKeydown($event)"></input>
                <span class="icon is-left">
                    <i class="fas fa-search"></i>
                </span>
            </p>
            <div class="dropdown-menu" role="menu">
                <div class="dropdown-content">
                    <a href="#"
                       class ="dropdown-item"
                       v-for="(ele, index) of displayElements"
                       v-bind:class="{'on-item-hover' : index == selectedOption}"
                       v-on:mouseover="selectedOption = index"
                       v-on:click="selectStock(ele.symbol, ele.name)">
                        <b>{{ ele.name }}</b> ({{ele.symbol}})
                    </a>
                </div>
            </div>
        </div>`
});

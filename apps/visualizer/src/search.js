import Vue from 'vue';

Vue.component('stock-search', {
    data: function() {
        return {
            symbol: ''
        }
    },
    methods: {
        input(e) {
            this.$data.symbol = e.target.value;

            // Perform stock search

            // Show drop down with elements.
        }
    },
    render: function(createElement) {
        const input = createElement('input', {
            class: 'input is-rounded',
            type: 'text',
            placeholder: 'GOOG',
            on: { input: this.input }
        });
        const icon = createElement('i', {
            class: 'fas fa-search',
            'aria-hidden': "true"
        });
        const span = createElement('span', {
            class: 'icon is-left'
        }, [icon]);
        const p = createElement('p', {class: 'control has-icons-left'}, [input, span]);
        return p;
    }
});

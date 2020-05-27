class Storage {

    static items = [
        {
            'id': 0,
            'brand': 'Nokia',
            'model': '3310',
            'price': '10 bazillion dollars',
        },
        {
            'id': 1,
            'brand': 'Samsung',
            'model': 'S15',
            'price': '15 pesos',
        },
        {
            'id': 2,
            'brand': 'Meskafonas',
            'model': 'X',
            'price': '1300 yen',
        },
        {
            'id': 3,
            'brand': 'Siemens',
            'model': 'C45',
            'price': '10000 rupees',
        },
        {
            'id': 4,
            'brand': 'Apple',
            'model': 'iPhone 9000',
            'price': '-15 bucks',
        },
    ];

    static getAll() {
        return this.items;
    }

    static get(id) {
        return this.items.find(x => x.id == id);
    }

    static add(item) {
        var id = Math.max(...this.items.map(x => x.id)) + 1;

        this.items.push({
            'id': id,
            'brand': item.brand,
            'model': item.model,
            'price': item.price,
        });

        return id;
    }

    static remove(id) {
        const pos = this.items.findIndex(x => x.id == id);

        if (pos > -1) {
            this.items.splice(pos, 1);
            return true;
        }

        return false;
    }

    static edit(id, item) {
        const pos = this.items.findIndex(x => x.id == id);

        if (pos > -1) {
            if (item.brand)
                this.items[pos].brand = item.brand;

            if (item.model)
                this.items[pos].model = item.model;

            if (item.price)
                this.items[pos].price = item.price;

            return true;
        }

        return false;
    }

    static replace(id, item) {
        const pos = this.items.findIndex(x => x.id == id);

        if (pos > -1) {
            item.id = Number.parseInt(id);
            this.items[pos] = item;
            return true;
        }
        
        return false;
    }
}

module.exports = Storage;
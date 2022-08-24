<template>
  <div class="section">
    <div class="container">

      <div class="field">
        <label class="label">Store</label>
        <div class="control">
          <input v-model="newProduct.store" type="text" class="input">
        </div>
      </div>

      <div class="field">
        <label class="label">Product</label>
        <div class="control">
          <input v-model="newProduct.product" type="text" class="input">
        </div>
      </div>

      <div class="columns">

        <div class="column">
          <div class="field">
            <label class="label">Price (Kroner)</label>
            <div class="control">
              <input v-model="newProduct.price" min="0" type="number" class="input">
            </div>
          </div>
        </div>

        <div class="column">
          <div class="field">
            <label class="label">Quantity</label>
            <div class="control">
              <input v-model="newProduct.quantity" min="0" type="number" class="input">
            </div>
          </div>
        </div>

        <div class="column">
          <div class="field">
            <label class="label">Total</label>
            <div class="control">
              <input v-model="getTotal" disabled class="input">
            </div>
          </div>
        </div>

      </div>

      <button @click="addProducts" class="button is-fullwidth">Add Product{{ multipleOrNot }}</button>
    
      <div v-if="products.length > 0">
        <hr>

        <table v-for="product in products" :key="product.product" class="table is-hoverable is-fullwidth">
          <thead>
            <tr>
              <th>Product</th>
              <th>Price</th>
              <th>Quantity</th>
              <th>Total</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>{{ product.product }}</td>
              <td>{{ product.price }} kr</td>
              <td>{{ product.quantity }}</td>
              <td>{{ product.total }}</td>
              <td><span style="cursor: pointer;" class="icon is-pulled-right"><i class="fa fa-times"></i></span></td>
            </tr>
          </tbody>
        </table>

      </div>

    </div>  
  </div>
  
</template>

<script>
export default {
    name: "NewReceipt",
    data() {
      return {
        newProduct: {
          store: null,
          product: "",
          category: null,
          price: null,
          quantity: 1
        },

        products: []
      }
    },

    methods: {
      resetNewProduct() {
        this.newProduct.product = "",
        this.newProduct.category = null,
        this.newProduct.price = null,
        this.newProduct.quantity = 1
      },

      addProducts() {
        if (this.newProduct.product === "") {
          alert("Product name cannot be empty")
          return
        } else if (isNaN(this.newProduct.product || this.newProduct.price !== 0)) {
          alert("Price cannot be zero")
          return
        } else if (this.newProduct.quantity === 0) {
          alert("Quantity cannot be zero")
          return
        }

        this.products.push(this.newProduct)
        this.resetNewProduct()
        console.log(this.products)
      }
    },

    computed: {
      getTotal() {
        var total = this.newProduct.product * this.newProduct.quantity
        return `${this.newProduct.price * this.newProduct.quantity} kr`
      },

      multipleOrNot() {
        if (this.newProduct.quantity === 1 || null || undefined) {
          return ""
        } else {
          return "s"
        }
      }
    }
}
</script>


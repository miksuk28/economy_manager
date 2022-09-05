<template>
  <div class="section">
    <div class="container">
      
      <div class="level">
        <div class="level-item has-text-centered mb-5">
          <div>
            <p class="heading">Total spending</p>
            <p class="title">{{ getTotalSpending() }} kr</p>
          </div>
        </div>
      </div>

      <button @click="this.$router.push('/receipts/new')" class="mb-5 has-background-primary button has-text-white is-fullwidth">Add Receipt</button>


      <div v-for="(receipt, index) in receipts" :key="receipt.id" class="card mb-3">
        <div class="card-content">
          <div class="columns">

            <div class="column">
              <div class="columns">
                <div class="column">
                  <button @click="receipt.viewProducts = !receipt.viewProducts" class="card-header-icon">
                    <span class="icon">
                      <i :class="chevronClass(receipt.viewProducts)"></i>
                    </span>
                  </button>
                </div>

                <div class="column">
                  <p class="has-text-weight-bold">Store</p>
                  <p class="">{{ receipt.store || "—"}}</p>
                </div>


              </div>
            </div>

            <div class="column">
              <div class="columns">
                <div class="column">
                  <p class="has-text-weight-bold">Quantity</p>
                  <p class="">{{ receipt.products.length }}</p>
                </div>

                <div class="column">
                  <p class="has-text-weight-bold">Category</p>
                  <p>—</p>
                </div>
              </div>
            </div>

            <div class="column has-text-right">
              <p class="has-text-weight-bold">Total</p>
              <p class="">{{ receipt.total }} kr</p>
            </div>
      
          </div>
        </div>

        <div class="section pt-0" v-if="receipt.viewProducts">
          <hr>
          <div v-for="product in receipt.products" :key="product.receipt_id" class="card-content">
            <div class="columns">
              <div class="column">
                <p>{{ product.item }}</p>
              </div>

              <div class="column">
                <p><span class="has-text-weight-bold">Quantity</span>: {{ product.quantity }}</p>
              </div>

              <div class="column">
                <p><span class="has-text-weight-bold">Price</span>: {{ product.price }} kr</p>
              </div>

              <div class="column">
                <p><span class="has-text-weight-bold">Total</span>: {{ product.total }} kr</p>
              </div>

              
            </div>

            <div class="columns">
              <button @click="deleteReceipt(receipt.id, index)" class="mt-5 has-background-danger button has-text-white is-fullwidth">Delete</button>
            </div>
          </div>
        </div>
        
      </div>
      
    </div>
  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "Receipts",
  data() {
    return {
      receipts: [],
    }
  },

  mounted() {
    this.getReceipts()
  },

  methods: {
    getReceipts() {
      axios.get("http://economy/api/receipts")
        .then((response) => {
          console.log(response.data)
          this.receipts = response.data
          this.resetProductsView()
        })
        .catch((error) => {
          console.log(error)
        })
    },

    removeReceiptLocal(index, id) {
      this.receipts.splice(index, 1)
    },

    deleteReceipt(id, index) {
      console.log(id)
      axios.delete("http://economy/api/receipt/" + id)
        .then((reponse) => {
          console.log(reponse.data)
        })
        .catch((error) => {
          console.log(error)
        })

      this.removeReceiptLocal(index)
    },

    resetProductsView() {
      this.receipts.forEach((item) => {
        item["viewProducts"] = false
      });
    },

    chevronClass(viewState) {
      return {
        "fa": true,
        "fa-angle-down": !viewState,
        "fa-angle-up": viewState
      }
    },

    getTotalSpending() {
      var total = 0;
      this.receipts.forEach((receipt) => {
        total += receipt.total
      });

      return Math.round(total * 100) /100
    }
  }
}
</script>
<style>

</style>
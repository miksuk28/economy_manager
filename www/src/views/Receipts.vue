<template>
  <h1>My Receipts</h1>
  <button @click="console.log(this.receipts)">CLICK</button>
</template>

<script>
export default {
  name: "Receipts"
}
</script>
  async created() {
    const response = await fetch("http://localhost:5000/receipts")
    const data = await response.json()
    this.receipts = data.total

    console.log(this.receipts)
  }


  data() {
    return {
      receipts: []
    }
  }
<style>

</style>
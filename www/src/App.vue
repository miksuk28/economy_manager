<template>

  <NavBar />
  <div class="container is-fluid">
    <router-view/>
  </div>
</template>

<script>
import NavBar from "./components/NavBar.vue"

export default {
  components: {
    NavBar
  }
}
</script>
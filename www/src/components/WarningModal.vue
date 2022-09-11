<template>
  <div class="modal">
    <div class="modal-background"></div>
    <div class="modal-content">

      <div class="card">
        <div class="card-content">
          <h1>{{ message }}</h1>
        </div>

        <footer class="card-footer">
          <a class="card-footer-item">OK</a>
        </footer>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: "WarningModal",
  props: ["message"]
}
</script>

<style>

</style>
<template>
  <v-snackbar
    v-model="snackbar.visible"
    :color="snackbar.color"
    :timeout="snackbar.timeout"
    location="bottom right"
    rounded="lg"
    elevation="4"
    min-width="300"
    max-width="440"
  >
    <div class="d-flex align-center ga-3">
      <v-icon v-if="snackbar.icon" :icon="snackbar.icon" size="20" color="white" />
      <span class="text-body-2 font-weight-medium text-white">{{ snackbar.message }}</span>
    </div>

    <template v-slot:actions>
      <v-btn
        icon="mdi-close"
        size="x-small"
        variant="text"
        color="white"
        @click="snackbar.hide()"
      />
    </template>
  </v-snackbar>
</template>

<script setup>
import { useSnackbarStore } from '@/stores/snackbar'
const snackbar = useSnackbarStore()
</script>

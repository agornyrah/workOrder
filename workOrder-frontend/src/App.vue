<template>
  <v-app class="app-wrapper">
    <Header />
    <v-main>
      <router-view />
    </v-main>
    <Footer />
    <SnackbarToast />
  </v-app>
</template>

<script setup>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
import SnackbarToast from '@/components/SnackbarToast.vue'
</script>

<style>
/* Import Manrope from Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&display=swap');

/* Force Manrope font globally and override Vuetify's default Roboto */
.app-wrapper,
.v-application {
  font-family: 'Manrope', sans-serif !important;
}

/* Override Vuetify's text utility classes */
.v-application .text-h1,
.v-application .text-h2,
.v-application .text-h3,
.v-application .text-h4,
.v-application .text-h5,
.v-application .text-h6,
.v-application .text-subtitle-1,
.v-application .text-subtitle-2,
.v-application .text-body-1,
.v-application .text-body-2,
.v-application .text-caption,
.v-application .text-overline,
.v-application .text-button {
  font-family: 'Manrope', sans-serif !important;
}

/* Ensure body also uses Manrope */
body {
  font-family: 'Manrope', sans-serif !important;
}
</style>

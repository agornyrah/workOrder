<template>
  <v-footer color="#064229" class="py-6">
    <v-container>
      <v-row class="d-flex align-center justify-center">
        <!-- Logo -->
        <v-col cols="12" sm="4" md="4" class="d-flex justify-center justify-sm-start">
          <router-link to="/" class="d-flex align-center text-decoration-none">
            <v-icon color="white" size="32" class="me-2">
              mdi-facebook-workplace
            </v-icon>
            <span class="font-weight-bold text-white">WorkOrder</span>
          </router-link>
        </v-col>

        <!-- Links -->
        <v-col cols="12" sm="4" md="4" class="d-flex justify-center ga-2">
          <v-btn variant="text" color="white" class="text-decoration-none" href="#">Privacy</v-btn>
          <v-btn variant="text" color="white" class="text-decoration-none" href="#">Support</v-btn>
          <v-btn variant="text" color="white" class="text-decoration-none" href="#">Contact</v-btn>
        </v-col>

        <!-- Copyright -->
        <v-col cols="12" sm="4" md="4" class="text-white text-center text-sm-right text-caption">
          &copy; 2026 WorkOrder Management System
        </v-col>
      </v-row>
    </v-container>
  </v-footer>
</template>

<script setup>

</script>
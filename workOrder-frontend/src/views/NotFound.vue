<template>
  <div>
    <!-- Brand Stripe -->
    <v-sheet height="4" color="#064229" class="w-100"></v-sheet>

    <v-container fluid class="pa-6 pa-md-8" style="max-width: 1005px;">
      <!-- Header -->
      <div class="mb-8">
        <div class="text-center text-md-left">
          <h1 class="font-weight-bold" style="color: #064229;">Oops Not Found</h1>
          <p style="color: #6b7c6b;">Try going back 
            <span><router-link to="/" class="text-decoration-none text-error">HOME</router-link></span>
          </p>
        </div>
      </div>
    </v-container>
    </div>
</template>

<style scoped>
.unread-entry {
  background: #f6fbf3;
}
</style>

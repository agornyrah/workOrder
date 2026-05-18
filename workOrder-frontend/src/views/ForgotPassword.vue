<template>
  <v-container class="fill-height">
    <v-row justify="center" align="center">
      <v-col cols="12" sm="6">
        <v-card class="pa-4" variant="flat">

          <!-- Logo Section -->
          <div class="text-center pa-4">
            <v-icon color="#064229" size="50" class="mb-2">
              mdi-facebook-workplace
            </v-icon>
            <h1 class="font-weight-bold mt-n2" style="color: #064229;">WorkOrder</h1>
          </div>

          <!-- Header -->
          <div class="text-center mb-6">
            <h1 class="text-h5 font-weight-bold" style="color: #064229;">Password Reset</h1>
            <p style="color: #6b7c6b;">Enter your email and we'll send a reset link.</p>
          </div>

          <!-- Success Message -->
          <v-alert
            v-if="emailSent"
            type="success"
            variant="tonal"
            class="mb-4"
            density="compact"
          >
            Reset link sent! Check your email.
          </v-alert>

          <!-- Forgot Password Form -->
          <v-form v-else ref="formRef" @submit.prevent="handleSubmit" v-model="isFormValid">
            <v-text-field
              v-model="email"
              label="Email address"
              type="email"
              variant="outlined"
              density="compact"
              class="mb-4"
              :rules="emailRules"
              hide-details="auto"
            ></v-text-field>

            <v-btn 
              type="submit"
              variant="flat"
              block
              color="#064229" 
              rounded="pill" 
              elevation="0"
              class="py-4"
              :disabled="!isFormValid || isLoading"
              :loading="isLoading"
            >
              Send reset link
            </v-btn>
          </v-form>

          <!-- Back to sign in -->
          <div class="text-center mt-4">
            <router-link to="/login" class="text-caption text-decoration-none text-primary">
              Back to sign in
            </router-link>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'

const formRef = ref()
const email = ref('')
const isFormValid = ref(false)
const isLoading = ref(false)
const emailSent = ref(false)

const emailRules = [
  (v) => !!v || 'Email is required',
  (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) || 'Enter a valid email address',
]

const handleSubmit = async () => {
  const isValid = await formRef.value?.validate()
  if (!isValid.valid) return

  isLoading.value = true

  // Simulate API call
  setTimeout(() => {
    isLoading.value = false
    emailSent.value = true
  }, 1500)
}
</script>

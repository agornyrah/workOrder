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
            <h1 class="text-h5 font-weight-bold" style="color: #064229;">Create Account</h1>
            <p style="color: #6b7c6b;">Join WorkOrder Management System</p>
          </div>

          <!-- Error Alert -->
          <v-alert
            v-if="errorMessage"
            type="error"
            variant="tonal"
            class="mb-4"
            density="compact"
          >
            {{ errorMessage }}
          </v-alert>

          <!-- Success Message -->
          <v-alert
            v-if="successMessage"
            type="success"
            variant="tonal"
            class="mb-4"
            density="compact"
          >
            {{ successMessage }}
          </v-alert>

          <!-- Signup Form -->
          <v-form v-else ref="formRef" @submit.prevent="handleSignup" v-model="isFormValid">
            <v-text-field
              v-model="name"
              label="Full name"
              variant="outlined"
              density="compact"
              class="mb-3"
              :rules="nameRules"
              hide-details="auto"
            ></v-text-field>

            <v-text-field
              v-model="email"
              label="Email address"
              type="email"
              variant="outlined"
              density="compact"
              class="mb-3"
              :rules="emailRules"
              hide-details="auto"
            ></v-text-field>

            <v-select
              v-model="role"
              label="Role"
              :items="roleOptions"
              variant="outlined"
              density="compact"
              class="mb-3"
              :rules="roleRules"
              hide-details="auto"
            ></v-select>

            <v-text-field
              v-model="password"
              label="Password"
              :type="showPassword ? 'text' : 'password'"
              variant="outlined"
              density="compact"
              class="mb-3"
              :rules="passwordRules"
              hide-details="auto"
              :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
              @click:append-inner="showPassword = !showPassword"
            ></v-text-field>

            <v-text-field
              v-model="confirmPassword"
              label="Confirm password"
              :type="showPassword ? 'text' : 'password'"
              variant="outlined"
              density="compact"
              class="mb-4"
              :rules="confirmPasswordRules"
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
              Create account
            </v-btn>
          </v-form>

          <!-- Sign in link -->
          <div class="text-center mt-4">
            <span class="text-body-2 text-grey-darken-1">Already have an account?</span>
            <router-link to="/login" class="text-body-2 text-decoration-none text-primary ms-1">
              Sign in
            </router-link>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const formRef = ref()

// Form state
const name = ref('')
const email = ref('')
const role = ref('')
const password = ref('')
const confirmPassword = ref('')
const showPassword = ref(false)
const isFormValid = ref(false)
const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

// Role options
const roleOptions = [
  { title: 'Administrator', value: 'admin' },
  { title: 'Supervisor', value: 'supervisor' },
  { title: 'Technician', value: 'technician' },
]

// Validation rules
const nameRules = [
  (v) => !!v || 'Name is required',
  (v) => v.length >= 2 || 'Name must be at least 2 characters',
]

const emailRules = [
  (v) => !!v || 'Email is required',
  (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) || 'Enter a valid email address',
]

const roleRules = [
  (v) => !!v || 'Role is required',
]

const passwordRules = [
  (v) => !!v || 'Password is required',
  (v) => v.length >= 6 || 'Password must be at least 6 characters',
]

const confirmPasswordRules = [
  (v) => !!v || 'Please confirm your password',
  (v) => v === password.value || 'Passwords do not match',
]

const handleSignup = async () => {
  const isValid = await formRef.value?.validate()
  if (!isValid.valid) return

  errorMessage.value = ''
  isLoading.value = true

  const result = await authStore.register({
    name: name.value,
    email: email.value,
    password: password.value,
    role: role.value,
  })

  isLoading.value = false

  if (!result.success) {
    errorMessage.value = result.error || 'Registration failed'
  } else {
    successMessage.value = 'Account created! Redirecting to login...'
    setTimeout(() => {
      router.push('/login')
    }, 2000)
  }
}
</script>

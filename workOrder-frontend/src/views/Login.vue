<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const formRef = ref()

// Form state
const email = ref('')
const password = ref('')
const showPassword = ref(false)
const rememberMe = ref(false)
const isFormValid = ref(false)
const errorMessage = ref('')

// Sync with auth store (must be computed to stay reactive)
const isLoading = computed(() => authStore.isLoading)

// Validation rules
const emailRules = [
  (value) => {
    if (!value) return 'Email is required'
    return true
  },
  (value) => {
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) return 'Enter a valid email address'
    return true
  },
]

const passwordRules = [
  (value) => {
    if (!value) return 'Password is required'
    return true
  },
]

// Load saved email if remember me was checked
onMounted(() => {
  const savedEmail = localStorage.getItem('rememberedEmail')
  if (savedEmail) {
    email.value = savedEmail
    rememberMe.value = true
  }
})

const handleLogin = async () => {
  // Validate form
  const isValid = await formRef.value?.validate()
  if (!isValid.valid) return

  // Clear any previous errors
  errorMessage.value = ''

  // Use auth store to login
  const result = await authStore.login(email.value, password.value)

  if (!result.success) {
    errorMessage.value = result.error || 'Login failed'
    return
  }

  // Redirect to dashboard on successful login
  router.push('/dashboard')

  // Save email to localStorage if remember me is checked
  if (result.success && rememberMe.value) {
    localStorage.setItem('rememberedEmail', email.value)
  } else if (!rememberMe.value) {
    localStorage.removeItem('rememberedEmail')
  }
}
</script>

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
            <p class="mt-n2" style="color: #064229;">Field Work Order Management</p>
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

          <!-- Login Form -->
          <v-form ref="formRef" @submit.prevent="handleLogin" v-model="isFormValid">
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

            <!-- Remember me & Forgot password -->
            <div class="d-flex flex-column flex-sm-row justify-space-between align-start align-sm-center mb-6 ga-2">
              <v-checkbox
                v-model="rememberMe"
                label="Remember me"
                density="compact"
                hide-details
                color="#064229"
                class="text-decoration-none"
              ></v-checkbox>
              <router-link to="/forgot-password" class="text-decoration-none text-error">
                Forgot password?
              </router-link>
            </div>

            <!-- Submit Button -->
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
              Sign In
            </v-btn>
          </v-form>

          <!-- Create account link -->
          <div class="text-center mt-4">
            <span class="text-grey-darken-1">Don't have an account?</span>
            <router-link to="/signup" class="text-decoration-none text-error ms-1">
              Create account
            </router-link>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
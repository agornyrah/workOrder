/**
 * auth.js — Authentication Store (Pinia)
 *
 * Manages user authentication state for the entire app.
 * Handles login, registration, logout, and session restoration.
 *
 * All auth requests are sent to the FastAPI backend via api.js.
 * The JWT token is stored in localStorage so the user stays
 * logged in even after a page refresh.
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { loginUser, registerUser, getCurrentUser } from '@/api'

export const useAuthStore = defineStore('auth', () => {

  // ── State ─────────────────────────────────────
  // Reactive variables that hold the current auth status

  const user = ref(null)                              // The logged-in user object (null = nobody)
  const token = ref(localStorage.getItem('token'))    // JWT token (restored from localStorage on load)
  const isLoading = ref(false)                        // True while an auth request is in progress
  const error = ref(null)                             // Holds the last error message (if any)

  // ── Getters ───────────────────────────────────
  // Computed properties that derive useful booleans from state

  const isAuthenticated = computed(() => !!token.value)                   // Is anyone logged in?
  const isAdmin = computed(() => user.value?.role === 'admin')            // Does the user have admin privileges?
  const isSupervisor = computed(() => user.value?.role === 'supervisor')  // Does the user have supervisor privileges?
  const isTechnician = computed(() => user.value?.role === 'technician')  // Is the user a technician?
  const userName = computed(() => user.value?.name || '')                 // Display name of the current user
  const userRole = computed(() => user.value?.role || '')                 // Role string of the current user

  // ── Actions ───────────────────────────────────

  /**
   * Register a new user account.
   * Sends the data to POST /auth/register via api.js.
   * @param {Object} data - { name, email, password, role }
   * @returns {{ success: boolean, error?: string }}
   */
  async function register(data) {
    isLoading.value = true
    error.value = null

    try {
      await registerUser(data)                        // POST /auth/register
      return { success: true }
    } catch (err) {
      // FastAPI returns errors in { detail: '...' } format
      error.value = err.response?.data?.detail || err.message || 'Registration failed'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Log in with email and password.
   * On success, stores the JWT token and user object.
   * @param {string} email
   * @param {string} password
   * @returns {{ success: boolean, error?: string }}
   */
  async function login(email, password) {
    isLoading.value = true
    error.value = null

    try {
      const data = await loginUser(email, password)   // POST /auth/login

      // Expected response shape: { access_token: '...', user: { id, email, name, role } }
      user.value = data.user
      token.value = data.access_token

      // Save to localStorage so the session survives page refreshes
      localStorage.setItem('token', data.access_token)
      localStorage.setItem('user', JSON.stringify(data.user))

      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Login failed'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Log out the current user.
   * Clears reactive state and removes persisted session data.
   */
  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  /**
   * Restore a previous session when the app first loads.
   * Called once in main.js during app bootstrap.
   * If a token and user are found in localStorage, they are loaded into state.
   */
  async function initAuth() {
    const savedToken = localStorage.getItem('token')
    const savedUser = localStorage.getItem('user')

    if (savedToken && savedUser) {
      token.value = savedToken
      try {
        user.value = JSON.parse(savedUser)

        // Optional: verify the token is still valid by asking the backend
        // const updatedUser = await getCurrentUser()   // GET /auth/me
        // user.value = updatedUser
      } catch {
        // If the saved data is corrupt, force a clean logout
        logout()
      }
    }
  }

  // ── Expose ────────────────────────────────────
  return {
    // State
    user,
    token,
    isLoading,
    error,
    // Getters
    isAuthenticated,
    isAdmin,
    isSupervisor,
    isTechnician,
    userName,
    userRole,
    // Actions
    register,
    login,
    logout,
    initAuth,
  }
})

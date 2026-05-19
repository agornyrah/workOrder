/**
 * api.js - Centralized API Service Layer
 *
 * This file creates a pre-configured Axios instance and exposes
 * functions for every FastAPI endpoint the app will eventually use.
 *
 * STATUS: ACTIVE — Wired into the stores.
 * The stores now use this service instead of localStorage.
 * Ensure your FastAPI server is running at the BASE_URL below.
 */

import axios from 'axios'

// ──────────────────────────────────────────────
//  Axios Instance
// ──────────────────────────────────────────────

const BASE_URL = 'http://localhost:8000' // Change this to your FastAPI server URL

export const api = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// ── Request Interceptor ──
// Automatically attaches the JWT token to every outgoing request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// ── Response Interceptor ──
// Handles common error scenarios globally (e.g. expired tokens)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // If the server says "Unauthorized", force a logout
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      // Optionally redirect to login — handled by router guards for now
    }
    return Promise.reject(error)
  }
)

// ══════════════════════════════════════════════
//  AUTH  ENDPOINTS
// ══════════════════════════════════════════════

/**
 * POST /auth/login
 * @param {string} email
 * @param {string} password
 * @returns {{ access_token: string, user: object }}
 */
export async function loginUser(email, password) {
  const response = await api.post('/auth/login', { email, password })
  return response.data
}

/**
 * POST /auth/register
 * @param {{ name: string, email: string, password: string, role: string }} data
 * @returns {{ id: string, email: string, name: string, role: string }}
 */
export async function registerUser(data) {
  const response = await api.post('/auth/register', data)
  return response.data
}

/**
 * GET /auth/me  — returns the currently authenticated user
 * @returns {{ id: string, email: string, name: string, role: string }}
 */
export async function getCurrentUser() {
  const response = await api.get('/auth/me')
  return response.data
}

// ══════════════════════════════════════════════
//  USER  ENDPOINTS
// ══════════════════════════════════════════════

/**
 * GET /users
 * @returns {Array<object>} list of all users
 */
export async function fetchUsers() {
  const response = await api.get('/users')
  return response.data
}

/**
 * GET /users/:id
 * @param {string} id
 * @returns {object} single user
 */
export async function fetchUserById(id) {
  const response = await api.get(`/users/${id}`)
  return response.data
}

/**
 * GET /users?role=technician — convenience wrapper
 * @returns {Array<object>} list of technicians
 */
export async function fetchTechnicians() {
  const response = await api.get('/users', { params: { role: 'technician' } })
  return response.data
}

/**
 * PUT /users/:id
 * @param {string} id
 * @param {object} updates
 * @returns {object} updated user
 */
export async function updateUser(id, updates) {
  const response = await api.put(`/users/${id}`, updates)
  return response.data
}

/**
 * DELETE /users/:id
 * @param {string} id
 * @returns {object} confirmation
 */
export async function deleteUser(id) {
  const response = await api.delete(`/users/${id}`)
  return response.data
}

// ══════════════════════════════════════════════
//  WORK  ORDER  ENDPOINTS
// ══════════════════════════════════════════════

/**
 * GET /workorders
 * @param {object} [params] — optional query filters (status, priority, site, search)
 * @returns {Array<object>} list of work orders
 */
export async function fetchWorkOrders(params = {}) {
  const response = await api.get('/workorders', { params })
  return response.data
}

/**
 * GET /workorders/:id
 * @param {string} id
 * @returns {object} single work order
 */
export async function fetchWorkOrderById(id) {
  const response = await api.get(`/workorders/${id}`)
  return response.data
}

/**
 * POST /workorders
 * @param {object} workOrderData
 * @returns {object} the newly created work order
 */
export async function createWorkOrder(workOrderData) {
  const response = await api.post('/workorders', workOrderData)
  return response.data
}

/**
 * PATCH /workorders/:id — partial update (edit fields, change status, etc.)
 * @param {string} id
 * @param {object} updates
 * @returns {object} updated work order
 */
export async function updateWorkOrder(id, updates) {
  const response = await api.patch(`/workorders/${id}`, updates)
  return response.data
}

/**
 * PATCH /workorders/:id/status — dedicated status change endpoint
 * @param {string} id
 * @param {string} status — new status value
 * @param {string} [notes] — optional completion notes
 * @returns {object} updated work order
 */
export async function updateWorkOrderStatus(id, status, notes = '') {
  const response = await api.patch(`/workorders/${id}/status`, { status, notes })
  return response.data
}

/**
 * DELETE /workorders/:id
 * @param {string} id
 * @returns {object} confirmation
 */
export async function deleteWorkOrder(id) {
  const response = await api.delete(`/workorders/${id}`)
  return response.data
}

// ══════════════════════════════════════════════
//  ACTIVITY  LOG  ENDPOINTS
// ══════════════════════════════════════════════

/**
 * GET /activity-log
 * @param {object} [params] — optional filters (limit, offset)
 * @returns {Array<object>} list of activity entries
 */
export async function fetchActivityLog(params = {}) {
  const response = await api.get('/activity-log', { params })
  return response.data
}

/**
 * POST /activity-log — create a log entry (server may also auto-generate these)
 * @param {object} entry — { action, workOrderId, workOrderTitle, performedBy, note }
 * @returns {object} the created log entry
 */
export async function createActivityLogEntry(entry) {
  const response = await api.post('/activity-log', entry)
  return response.data
}

/**
 * PATCH /activity-log/read-all — mark all entries as read for the current user
 * @returns {object} confirmation
 */
export async function markAllActivityRead() {
  const response = await api.patch('/activity-log/read-all')
  return response.data
}

/**
 * PATCH /activity-log/:id/read — mark a single entry as read
 * @param {string} id
 * @returns {object} confirmation
 */
export async function markActivityRead(id) {
  const response = await api.patch(`/activity-log/${id}/read`)
  return response.data
}

/**
 * DELETE /activity-log
 * @returns {object} confirmation
 */
export async function clearActivityLog() {
  const response = await api.delete('/activity-log')
  return response.data
}

// ══════════════════════════════════════════════
//  DEFAULT EXPORT  (for convenience)
// ══════════════════════════════════════════════

export default api

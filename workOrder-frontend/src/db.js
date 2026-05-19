// db.js
// Lightweight compatibility layer used by a few legacy views.
// This bridges to the real API and returns an array of technicians:
// [{ user_id, name }]

import { fetchTechnicians } from './api'

export async function getTechnicians() {
  try {
    const users = await fetchTechnicians()
    return users.map(u => ({ user_id: u.id, name: u.name }))
  } catch (err) {
    console.error('Failed to load technicians', err)
    return []
  }
}



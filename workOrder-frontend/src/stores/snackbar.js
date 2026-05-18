import { defineStore } from 'pinia' // Getting the toy box maker
import { ref } from 'vue' // Getting a tool to remember things

export const useSnackbarStore = defineStore('snackbar', () => { // Making our announcement box
  const visible = ref(false) // Is the message showing right now? (Start with no)
  const message = ref('') // What does the message say? (Start with nothing)
  const color = ref('success') // What color is the message? (Green for good!)
  const icon = ref('') // What picture is next to the message?
  const timeout = ref(3500) // How long does the message stay? (A few seconds)

  /**
   * Show a toast notification. // This shows our message on the screen
   * @param {string|Object} options - message string or { message, color, icon, timeout } // Information we give it
   */
  function show(options) { // This is the button to show a message
    if (typeof options === 'string') { // If we just give it a simple sentence...
      message.value = options // Use that sentence as the message
      color.value = 'success' // Make it green
      icon.value = 'mdi-check-circle-outline' // Put a checkmark
      timeout.value = 3000 // Wait a bit before it disappears
    } else { // If we give it a whole list of choices...
      message.value = options.message || '' // Use the message they gave us
      color.value = options.color || 'success' // Use the color they gave us
      icon.value = options.icon || iconForColor(options.color) // Use their picture or pick one
      timeout.value = options.timeout ?? 3000 // Use their time or use our default
    } // End of choices
    visible.value = true // Okay, now show the message!
  } // End of the button code

  function success(msg) { // A quick button for "Good job!" messages
    show({ message: msg, color: '#064229', icon: 'mdi-check-circle-outline' }) // Show a green message
  } // End

  function error(msg) { // A quick button for "Uh oh!" messages
    show({ message: msg, color: 'error', icon: 'mdi-alert-circle-outline' }) // Show a red message
  } // End

  function info(msg) { // A quick button for just telling someone something
    show({ message: msg, color: 'blue-darken-1', icon: 'mdi-information-outline' }) // Show a blue message
  } // End

  function warning(msg) { // A quick button for "Be careful!" messages
    show({ message: msg, color: 'orange-darken-2', icon: 'mdi-alert-outline' }) // Show an orange message
  } // End

  function hide() { // A button to make the message go away early
    visible.value = false // Hide it!
  } // End

  function iconForColor(c) { // A helper to pick a picture based on the color
    if (!c) return 'mdi-check-circle-outline' // If no color, use a checkmark
    if (c.includes('error') || c.includes('red')) return 'mdi-alert-circle-outline' // Red gets an exclamation
    if (c.includes('orange') || c.includes('warning')) return 'mdi-alert-outline' // Orange gets a triangle
    if (c.includes('blue')) return 'mdi-information-outline' // Blue gets an "i"
    return 'mdi-check-circle-outline' // Otherwise, just use a checkmark
  } // End of helper

  return { visible, message, color, icon, timeout, show, success, error, info, warning, hide } // Share all these tools!
}) // End of box maker
// Done!

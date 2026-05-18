import { defineStore } from 'pinia' // We are getting a special toy box maker from Pinia
import { ref, computed } from 'vue' // We are getting tools to help our toys change and grow

export const useAppStore = defineStore('app', () => { // We are making a new toy box called 'app'
  // State 
  // This part is for keeping things inside
  const count = ref(0) // We have a counter that starts at zero
  const title = ref('Vuetify Workorder App') // This is the name of our project

  // Getters 
  // This part is for looking at things in a new way
  const doubleCount = computed(() => count.value * 2) // This is a magic trick that always doubles our count

  // Actions 
  // This part is for doing things with our toys
  function increment() { // This is a button to make our count go up
    count.value++ // Add one more to our count!
  } // End of the button code

  function decrement() { // This is a button to make our count go down
    count.value-- // Take away one from our count!
  } // End of the button code

  return { // Now we share all our toys with the rest of the app
    count, // Give them the count
    title, // Give them the title
    doubleCount, // Give them the magic doubling trick
    increment, // Give them the "go up" button
    decrement, // Give them the "go down" button
  }
})

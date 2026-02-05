<script setup lang="ts">
/**
 * TruEditor - Animated Counter Component
 * =======================================
 * Number counter with smooth animation (counting up effect).
 */

import { ref, watch, onMounted } from 'vue'

interface Props {
  /** Target value to count to */
  value: number
  /** Animation duration in milliseconds */
  duration?: number
  /** Decimal places */
  decimals?: number
  /** Prefix (e.g., '$') */
  prefix?: string
  /** Suffix (e.g., '%') */
  suffix?: string
  /** Thousand separator */
  separator?: string
  /** Start animation on mount */
  autoStart?: boolean
  /** Easing function type */
  easing?: 'linear' | 'easeOut' | 'easeInOut'
}

const props = withDefaults(defineProps<Props>(), {
  duration: 1000,
  decimals: 0,
  prefix: '',
  suffix: '',
  separator: ',',
  autoStart: true,
  easing: 'easeOut',
})

const emit = defineEmits<{
  complete: []
}>()

const displayValue = ref(0)
const isAnimating = ref(false)

// Easing functions
const easingFunctions = {
  linear: (t: number) => t,
  easeOut: (t: number) => 1 - Math.pow(1 - t, 3),
  easeInOut: (t: number) => t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2,
}

/**
 * Format number with separator and decimals
 */
function formatNumber(num: number): string {
  const fixed = num.toFixed(props.decimals)
  const parts = fixed.split('.')
  const integerPart = parts[0] ?? '0'
  parts[0] = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, props.separator)
  return parts.join('.')
}

/**
 * Animate the counter
 */
function animate(from: number, to: number): void {
  if (isAnimating.value) return
  
  isAnimating.value = true
  const startTime = performance.now()
  const easingFn = easingFunctions[props.easing]
  
  function step(currentTime: number): void {
    const elapsed = currentTime - startTime
    const progress = Math.min(elapsed / props.duration, 1)
    const easedProgress = easingFn(progress)
    
    displayValue.value = from + (to - from) * easedProgress
    
    if (progress < 1) {
      requestAnimationFrame(step)
    } else {
      displayValue.value = to
      isAnimating.value = false
      emit('complete')
    }
  }
  
  requestAnimationFrame(step)
}

/**
 * Start the counter animation
 */
function start(): void {
  animate(0, props.value)
}

/**
 * Reset the counter
 */
function reset(): void {
  displayValue.value = 0
}

// Watch for value changes
watch(() => props.value, (newValue, oldValue) => {
  animate(oldValue ?? 0, newValue ?? 0)
})

// Auto start on mount
onMounted(() => {
  if (props.autoStart) {
    start()
  }
})

// Expose methods
defineExpose({
  start,
  reset,
})
</script>

<template>
  <span class="animated-counter">
    {{ prefix }}{{ formatNumber(displayValue) }}{{ suffix }}
  </span>
</template>

<style scoped>
.animated-counter {
  font-variant-numeric: tabular-nums;
}
</style>

<template>
  <div class="app-container">
    <header class="app-header">
      <div class="header-content">
        <div class="header-left">
          <div class="logo">
            <h1 class="logo-text">智能面试官</h1>
            <p class="logo-subtitle">AI Interview Assistant</p>
          </div>
        </div>
        <div class="header-right">
          <slot name="header-right"></slot>
        </div>
      </div>
    </header>

    <main class="main-content">
      <slot />
    </main>

    <footer class="app-footer">
      <div class="footer-content">
        <p>&copy; 2025 智能面试官 - 让面试更智能、更高效</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
</script>

<style scoped>
.app-header {
  background: var(--card-bg);
  border-bottom: 1px solid var(--border-primary);
  box-shadow: var(--card-shadow);
  position: sticky;
  top: 0;
  z-index: 50;
  backdrop-filter: blur(10px);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md) var(--spacing-xl);
  max-width: 1400px;
  margin: 0 auto;
}

.header-left {
  display: flex;
  align-items: center;
}

.logo {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.logo-text {
  font-size: var(--font-size-xl);
  font-weight: 700;
  color: var(--primary-600);
  margin: 0;
  line-height: 1.2;
}

.logo-subtitle {
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
  margin: 0;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.app-footer {
  background: var(--card-bg);
  border-top: 1px solid var(--border-primary);
  margin-top: auto;
}

.footer-content {
  text-align: center;
  padding: var(--spacing-lg) var(--spacing-xl);
  max-width: 1400px;
  margin: 0 auto;
}

.footer-content p {
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
  margin: 0;
}

@media (max-width: 768px) {
  .header-content {
    padding: var(--spacing-md);
  }
  
  .logo-text {
    font-size: var(--font-size-lg);
  }
  
  .logo-subtitle {
    display: none;
  }
  
  .footer-content {
    padding: var(--spacing-md);
  }
}
</style>

const body = document.body;

function applyTheme(theme) {
    const root = document.documentElement;
    if (theme === 'light') {

      body.classList.replace('dark-mode', 'light-mode');
    } else {

      body.classList.replace('light-mode', 'dark-mode');
    }
  }

  function toggleTheme() {
    const currentTheme = localStorage.getItem('theme');
    if (currentTheme === 'light') {
      localStorage.setItem('theme', 'dark');
      applyTheme('dark');
    } else {
      localStorage.setItem('theme', 'light');
      applyTheme('light');
    }
  }

  // Check if a theme preference exists in local storage
  const savedTheme = localStorage.getItem('theme');

  // Apply the saved theme or the default theme (dark mode)
  applyTheme(savedTheme || 'dark');

  // Listen for the button click and toggle the theme
  const themeToggleBtn = document.getElementById('themeToggleBtn');
  themeToggleBtn.addEventListener('click', toggleTheme);

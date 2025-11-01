// Solarpunk Odyssey: Binary Terraforming System
// A vision of harmonious space exploration and planetary renewal

// Generate life-seed pattern (deterministic but organic-feeling)
function generateLifePattern(bits) {
  const pattern = [];
  let seed = 0x5EED; // SEED in hex-like
  for (let i = 0; i < bits; i++) {
    seed = (seed * 1103515245 + 12345) & 0x7fffffff;
    pattern.push(seed % 2);
  }
  return pattern;
}

// Base patterns for different scales
const SEED_PATTERN = generateLifePattern(560); // 70 bytes
let warpActive = true;
let currentSpeed = 'cruise';
let currentView = 'all';

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
  initializeStarfield();
  generateAllBiospheres();
  createQuantumGarden();
  startTerraformingAnimation();
  animateBiodomeStats();
});

// Generate all biosphere patterns
function generateAllBiospheres() {
  // 70-byte seed pattern
  generateBiosphere('orbit70', SEED_PATTERN.slice(0, 560), 560);
  generateWarpPattern('warp-layer70-1', SEED_PATTERN.slice(0, 560), 8);
  generateWarpPattern('warp-layer70-2', SEED_PATTERN.slice(0, 560), 8);
  
  // 140-byte expansion
  const expansion140 = [...SEED_PATTERN, ...SEED_PATTERN];
  generateBiosphere('orbit140', expansion140.slice(0, 1120), 1120);
  generateWarpPattern('warp-layer140-1', expansion140.slice(0, 1120), 6);
  generateWarpPattern('warp-layer140-2', expansion140.slice(0, 1120), 6);
  
  // 280-byte civilization
  const civilization280 = [...expansion140, ...expansion140];
  generateBiosphere('orbit280', civilization280.slice(0, 2240), 2240);
  generateWarpPattern('warp-layer280-1', civilization280.slice(0, 2240), 5);
  generateWarpPattern('warp-layer280-2', civilization280.slice(0, 2240), 5);
}

// Generate a biosphere display (like a planet's ecosystem)
function generateBiosphere(elementId, pattern, maxBits) {
  const container = document.getElementById(elementId);
  if (!container) return;
  
  container.innerHTML = '';
  const bitsToShow = Math.min(pattern.length, maxBits);
  
  for (let i = 0; i < bitsToShow; i++) {
    const planet = document.createElement('span');
    planet.className = `planet-bit planet-bit-${pattern[i]}`;
    planet.textContent = pattern[i];
    planet.style.animationDelay = `${i * 0.02}s`;
    planet.title = pattern[i] === 1 ? 'Life-bearing world' : 'Potential for life';
    container.appendChild(planet);
  }
  
  // Add infinity indicator for endless growth
  if (pattern.length > maxBits) {
    const infinity = document.createElement('span');
    infinity.style.fontSize = '1.8rem';
    infinity.style.margin = '0 15px';
    infinity.style.color = 'var(--solar-gold)';
    infinity.textContent = '... ∞ 🌌';
    container.appendChild(infinity);
  }
}

// Generate warp drive pattern (faster-than-light travel visualization)
function generateWarpPattern(elementId, pattern, repetitions) {
  const container = document.getElementById(elementId);
  if (!container) return;
  
  container.innerHTML = '';
  
  for (let rep = 0; rep < repetitions; rep++) {
    const row = document.createElement('div');
    row.className = 'orbital-ring';
    row.style.margin = '8px 0';
    
    // Show subset of pattern for warp effect
    const subset = pattern.slice(0, Math.min(pattern.length, 80));
    subset.forEach((bit, i) => {
      const planet = document.createElement('span');
      planet.className = `planet-bit planet-bit-${bit}`;
      planet.textContent = bit;
      planet.style.opacity = 1 - (rep * 0.1);
      row.appendChild(planet);
    });
    
    container.appendChild(row);
  }
}

// Create quantum garden (living nodes)
function createQuantumGarden() {
  const garden = document.getElementById('quantumGarden');
  if (!garden) return;
  
  for (let i = 0; i < 24; i++) {
    const node = document.createElement('div');
    node.className = 'seed-node';
    node.style.animationDelay = `${i * 0.15}s`;
    node.title = 'Living quantum node';
    
    node.addEventListener('click', function() {
      this.style.transform = 'scale(1.5) rotate(360deg)';
      this.style.boxShadow = '0 0 40px var(--solar-gold)';
      setTimeout(() => {
        this.style.transform = '';
        this.style.boxShadow = '';
      }, 600);
    });
    
    garden.appendChild(node);
  }
}

// Initialize starfield background
function initializeStarfield() {
  // Starfield is handled by CSS, but we can add dynamic elements
  console.log('🌟 Starfield initialized - Navigation systems online');
}

// Start terraforming animation
function startTerraformingAnimation() {
  const warpDrives = document.querySelectorAll('.warp-layer');
  warpDrives.forEach(layer => {
    layer.style.animationPlayState = warpActive ? 'running' : 'paused';
  });
}

// Toggle warp drive
function toggleWarpDrive() {
  warpActive = !warpActive;
  const warpDrives = document.querySelectorAll('.warp-layer');
  warpDrives.forEach(layer => {
    layer.style.animationPlayState = warpActive ? 'running' : 'paused';
  });
  
  console.log(`🚀 Warp drive ${warpActive ? 'engaged' : 'disengaged'}`);
  showNotification(`Warp Drive ${warpActive ? 'Engaged' : 'Disengaged'}`);
}

// Adjust travel speed
function adjustSpeed(speed) {
  currentSpeed = speed;
  const warpDrives = document.querySelectorAll('.warp-layer');
  
  let duration;
  switch(speed) {
    case 'fast':
      duration = '8s';
      break;
    case 'cruise':
      duration = '15s';
      break;
    default:
      duration = '15s';
  }
  
  warpDrives.forEach(layer => {
    layer.style.animationDuration = duration;
  });
  
  console.log(`⚡ Speed adjusted to ${speed} mode`);
  showNotification(`Speed: ${speed.toUpperCase()} mode`);
}

// Regenerate terraform pattern
function regenerateTerraform() {
  const newPattern = [];
  for (let i = 0; i < 560; i++) {
    newPattern.push(Math.random() > 0.5 ? 1 : 0);
  }
  
  generateBiosphere('orbit70', newPattern, 560);
  
  const expansion140 = [...newPattern, ...newPattern];
  generateBiosphere('orbit140', expansion140, 1120);
  
  const civilization280 = [...expansion140, ...expansion140];
  generateBiosphere('orbit280', civilization280, 2240);
  
  // Regenerate warp patterns
  generateWarpPattern('warp-layer70-1', newPattern, 8);
  generateWarpPattern('warp-layer70-2', newPattern, 8);
  generateWarpPattern('warp-layer140-1', expansion140, 6);
  generateWarpPattern('warp-layer140-2', expansion140, 6);
  generateWarpPattern('warp-layer280-1', civilization280, 5);
  generateWarpPattern('warp-layer280-2', civilization280, 5);
  
  console.log('🌱 New biosphere generated');
  showNotification('Biosphere Regenerated');
}

// Switch view between different scales
function switchView() {
  const views = ['all', '70', '140', '280'];
  const currentIndex = views.indexOf(currentView);
  currentView = views[(currentIndex + 1) % views.length];
  
  const station70 = document.getElementById('station70');
  const station140 = document.getElementById('station140');
  const station280 = document.getElementById('station280');
  
  switch(currentView) {
    case '70':
      station70.style.display = 'block';
      station140.style.display = 'none';
      station280.style.display = 'none';
      break;
    case '140':
      station70.style.display = 'none';
      station140.style.display = 'block';
      station280.style.display = 'none';
      break;
    case '280':
      station70.style.display = 'none';
      station140.style.display = 'none';
      station280.style.display = 'block';
      break;
    default:
      station70.style.display = 'block';
      station140.style.display = 'block';
      station280.style.display = 'block';
  }
  
  console.log(`🔭 View switched to ${currentView}`);
  showNotification(`View: ${currentView.toUpperCase()}`);
}

// Animate biodome statistics
function animateBiodomeStats() {
  const stats = ['oxygenLevel', 'solarCapture'];
  
  stats.forEach(statId => {
    const element = document.getElementById(statId);
    if (!element) return;
    
    let value = 95;
    const interval = setInterval(() => {
      value += Math.random() * 2 - 1;
      value = Math.max(95, Math.min(100, value));
      element.textContent = `${value.toFixed(1)}%`;
      
      if (value >= 99.5) {
        element.textContent = '100%';
      }
    }, 2000);
  });
  
  // Animate biodiversity to infinity
  const biodiversity = document.getElementById('biodiversity');
  if (biodiversity) {
    let count = 0;
    const interval = setInterval(() => {
      count += Math.floor(Math.random() * 100) + 50;
      biodiversity.textContent = count.toLocaleString();
      
      if (count > 999999) {
        clearInterval(interval);
        biodiversity.textContent = '∞';
      }
    }, 150);
  }
}

// Show notification
function showNotification(message) {
  const notification = document.createElement('div');
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: linear-gradient(135deg, var(--solar-green), var(--earth-teal));
    color: #0a0e27;
    padding: 15px 25px;
    border-radius: 10px;
    font-weight: bold;
    box-shadow: 0 0 30px rgba(127, 255, 0, 0.5);
    z-index: 1000;
    animation: slideIn 0.3s ease-out;
  `;
  notification.textContent = message;
  document.body.appendChild(notification);
  
  setTimeout(() => {
    notification.style.animation = 'slideOut 0.3s ease-out';
    setTimeout(() => notification.remove(), 300);
  }, 2000);
}

// Add click interaction to planet bits
document.addEventListener('click', function(e) {
  if (e.target.classList.contains('planet-bit')) {
    const currentValue = e.target.textContent;
    const newValue = currentValue === '0' ? '1' : '0';
    e.target.textContent = newValue;
    e.target.className = `planet-bit planet-bit-${newValue}`;
    
    // Terraform effect
    e.target.style.transition = 'all 0.3s';
    e.target.style.transform = 'scale(1.8) rotate(360deg)';
    setTimeout(() => {
      e.target.style.transform = '';
    }, 300);
  }
});

// Keyboard shortcuts for navigation
document.addEventListener('keydown', function(e) {
  switch(e.key.toLowerCase()) {
    case ' ':
      e.preventDefault();
      toggleWarpDrive();
      break;
    case 'f':
      adjustSpeed('fast');
      break;
    case 'c':
      adjustSpeed('cruise');
      break;
    case 'r':
      regenerateTerraform();
      break;
    case 'v':
      switchView();
      break;
  }
});

// Console welcome message
console.log(`
╔═══════════════════════════════════════════════════════════╗
║              SOLARPUNK ODYSSEY v∞.∞.∞                    ║
║                                                           ║
║  "Every seed contains a forest"                          ║
║  "Every forest contains a world"                         ║
║  "Every world contains infinite possibilities"           ║
║                                                           ║
║  Navigation Controls:                                    ║
║  [SPACE] - Toggle Warp Drive                             ║
║  [F]     - Fast Mode                                     ║
║  [C]     - Cruise Mode                                   ║
║  [R]     - Regenerate Biosphere                          ║
║  [V]     - Switch View                                   ║
║                                                           ║
║  Click any planet to terraform it                        ║
║  Click quantum nodes to activate them                    ║
║                                                           ║
║  🌱 → 🌳 → 🌍 → 🌌 → ∞                                   ║
╚═══════════════════════════════════════════════════════════╝
`);

// Add CSS animations dynamically
const style = document.createElement('style');
style.textContent = `
  @keyframes slideIn {
    from { transform: translateX(400px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
  }
  
  @keyframes slideOut {
    from { transform: translateX(0); opacity: 1; }
    to { transform: translateX(400px); opacity: 0; }
  }
`;
document.head.appendChild(style);

// Export for potential external use
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    generateLifePattern,
    toggleWarpDrive,
    adjustSpeed,
    regenerateTerraform,
    switchView
  };
}
</script>
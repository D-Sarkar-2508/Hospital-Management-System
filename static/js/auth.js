// DS Hospital – Auth JS

let currentRole = '';

const ROLE_LABELS = {
  patient: '🧑‍⚕️ Patient',
  doctor: '👨‍⚕️ Doctor',
  pharmacist: '💊 Pharmacist',
  receptionist: '📋 Receptionist',
  admin: '🛡️ Admin'
};

function openModal(role) {
  currentRole = role;
  document.getElementById('roleLabel').textContent = ROLE_LABELS[role];
  // Patient registration has DOB, others don't
  document.getElementById('dobField').style.display = role === 'patient' ? 'block' : 'none';
  switchTab('login');
  document.getElementById('authModal').style.display = 'flex';
  // Clear previous inputs
  document.getElementById('loginIdentifier').value = '';
  document.getElementById('loginPassword').value = '';
  // Set max date for DOB (today)
  const today = new Date().toISOString().split('T')[0];
  document.getElementById('regDOB').max = today;
  // Clear messages
  document.getElementById('loginMsg').textContent = '';
  document.getElementById('registerMsg').textContent = '';
  // Render history saved under this specific role
  renderHistoryDatalist();
}

function closeModal() {
  document.getElementById('authModal').style.display = 'none';
}

function switchTab(tab) {
  document.getElementById('loginForm').style.display = tab === 'login' ? 'block' : 'none';
  document.getElementById('registerForm').style.display = tab === 'register' ? 'block' : 'none';
  document.getElementById('loginTab').classList.toggle('active', tab === 'login');
  document.getElementById('registerTab').classList.toggle('active', tab === 'register');
}

// Dynamic UI script to draw history inside the datalist block
function renderHistoryDatalist() {
  const datalist = document.getElementById('user-history');
  datalist.innerHTML = ''; // Reset frame
  
  // Extract specific role mapping from local storage records
  const storageKey = `ds_hospital_history_${currentRole}`;
  const localData = localStorage.getItem(storageKey);
  
  if (localData) {
    try {
      const credentialMap = JSON.parse(localData);
      // Generate option structures for each stored item
      Object.keys(credentialMap).forEach(uid => {
        const option = document.createElement('option');
        option.value = uid;
        option.setAttribute('data-password', credentialMap[uid]);
        datalist.appendChild(option);
      });
    } catch(e) {
      console.error("Error loading saved credentials history", e);
    }
  }
}

// Event triggered when a user picks an element from the dropdown arrow
function autoFillPassword() {
  const inputVal = document.getElementById('loginIdentifier').value;
  const options = document.querySelectorAll('#user-history option');
  const passwordField = document.getElementById('loginPassword');
  
  for (let i = 0; i < options.length; i++) {
    if (options[i].value === inputVal) {
      const savedPassword = options[i].getAttribute('data-password');
      if (savedPassword) {
        passwordField.value = savedPassword;
      }
      break;
    }
  }
}

// ── Validation helpers ──

function validateContact(c) {
  return /^\d{10}$/.test(c);
}

function validateEmail(e) {
  // lowercase letters, digits and @gmail.com
  return /^[a-z0-9]+@gmail\.com$/.test(e);
}

function validatePassword(p) {
  // letters + digits + special characters, min 8
  const hasLetter = /[a-zA-Z]/.test(p);
  const hasDigit = /\d/.test(p);
  const hasSpecial = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(p);
  return p.length >= 8 && hasLetter && hasDigit && hasSpecial;
}

// ── Login ──

function doLogin() {
  const identifier = document.getElementById('loginIdentifier').value.trim();
  const password = document.getElementById('loginPassword').value;
  const msg = document.getElementById('loginMsg');

  if (!identifier || !password) {
    msg.style.color = '#ef4444';
    msg.textContent = 'Please fill all fields.';
    return;
  }

  msg.style.color = '#6b7f94';
  msg.textContent = 'Logging in...';

  fetch('/api/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ role: currentRole, identifier, password })
  })
    .then(r => r.json())
    .then(data => {
      if (data.success) {
        // --- PERSISTENCE STORAGE INJECTION ---
        const storageKey = `ds_hospital_history_${currentRole}`;
        let historyDict = {};
        
        try {
          const currentHistory = localStorage.getItem(storageKey);
          if (currentHistory) historyDict = JSON.parse(currentHistory);
        } catch(e) { historyDict = {}; }

        // Append the working pair combination cleanly
        historyDict[identifier] = password;
        localStorage.setItem(storageKey, JSON.stringify(historyDict));
        // -------------------------------------

        msg.style.color = '#22c55e';
        msg.textContent = 'Login successful! Redirecting...';
        setTimeout(() => { window.location.href = data.redirect; }, 800);
      } else {
        msg.style.color = '#ef4444';
        msg.textContent = data.message || 'Invalid credentials!';
      }
    })
    .catch(() => {
      msg.style.color = '#ef4444';
      msg.textContent = 'Server error. Try again.';
    });
}

// ── Register ──

function doRegister() {
  const name = document.getElementById('regName').value.trim();
  const address = document.getElementById('regAddress').value.trim();
  const contact = document.getElementById('regContact').value.trim();
  const dob = document.getElementById('regDOB').value;
  const email = document.getElementById('regEmail').value.trim();
  const password = document.getElementById('regPassword').value;
  const msg = document.getElementById('registerMsg');

  // Validations
  if (!name || !contact || !email || !password) {
    msg.style.color = '#ef4444';
    msg.textContent = 'Please fill all required fields.';
    return;
  }
  if (currentRole === 'patient' && !dob) {
    msg.style.color = '#ef4444';
    msg.textContent = 'Please select date of birth.';
    return;
  }
  if (!validateContact(contact)) {
    msg.style.color = '#ef4444';
    msg.textContent = 'Contact number must be exactly 10 digits.';
    return;
  }
  if (!validateEmail(email)) {
    msg.style.color = '#ef4444';
    msg.textContent = 'Email must be lowercase letters/digits + @gmail.com (e.g. john99@gmail.com)';
    return;
  }
  if (!validatePassword(password)) {
    msg.style.color = '#ef4444';
    msg.textContent = 'Password must be at least 8 characters with letters, digits & special characters.';
    return;
  }

  msg.style.color = '#6b7f94';
  msg.textContent = 'Registering...';

  fetch('/api/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ role: currentRole, name, address, contact, dob, email, password })
  })
    .then(r => r.json())
    .then(data => {
      if (data.success) {
        msg.style.color = '#22c55e';
        msg.textContent = '✅ ' + data.message + ' You can now login.';
        // Clear form
        ['regName','regAddress','regContact','regDOB','regEmail','regPassword'].forEach(id => {
          document.getElementById(id).value = '';
        });
        setTimeout(() => switchTab('login'), 2000);
      } else {
        msg.style.color = '#ef4444';
        msg.textContent = data.message || 'Registration failed.';
      }
    })
    .catch(() => {
      msg.style.color = '#ef4444';
      msg.textContent = 'Server error. Try again.';
    });
}

// Close modal on overlay click
document.getElementById('authModal').addEventListener('click', function(e) {
  if (e.target === this) closeModal();
});

// Enter key support
document.addEventListener('keydown', function(e) {
  if (e.key === 'Enter') {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    if (loginForm.style.display !== 'none') doLogin();
    else if (registerForm.style.display !== 'none') doRegister();
  }
});

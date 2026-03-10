function initStorage() {
  if (!localStorage.getItem('users')) {
    localStorage.setItem('users', JSON.stringify([
      { id:1, username:'admin',  password:'admin',  role:'admin' },
      { id:2, username:'user1',  password:'pass',   role:'user'  }
    ]));
  }
  if (!localStorage.getItem('tickets')) {
    localStorage.setItem('tickets', JSON.stringify([]));
  }
}

function getUsers()          { return JSON.parse(localStorage.getItem('users')   || '[]'); }
function saveUsers(users)    { localStorage.setItem('users',   JSON.stringify(users));   }
function getTickets()        { return JSON.parse(localStorage.getItem('tickets') || '[]'); }
function saveTickets(tickets){ localStorage.setItem('tickets', JSON.stringify(tickets)); }

function getCurrentUser()    { return JSON.parse(localStorage.getItem('currentUser') || 'null'); }
function isLoggedIn()        { return !!getCurrentUser(); }

function login(username, password) {
  const user = getUsers().find(u => u.username === username && u.password === password);
  if (user) {
    localStorage.setItem('currentUser', JSON.stringify(user));
    return { success: true, role: user.role };
  }
  return { success: false, message: 'Invalid username or password' };
}

function logout() {
  localStorage.removeItem('currentUser');
  window.location.href = '/index.html';
}

function createTicket(title, desc, userId) {
  const tickets = getTickets();
  tickets.push({
    id: Date.now(),
    title,
    desc,
    status: 'Open',
    priority: 'Low',
    createdBy: userId,
    createdAt: new Date().toISOString()
  });
  saveTickets(tickets);
}

function addUser(username, password) {
  const users = getUsers();
  if (users.some(u => u.username === username)) {
    alert('Username already exists');
    return;
  }
  const id = Math.max(0, ...users.map(u => u.id)) + 1;
  users.push({ id, username, password, role: 'user' });
  saveUsers(users);
  alert('User created successfully');
}

function deleteUser(id) {
  if (!confirm('Delete this user?')) return;
  saveUsers(getUsers().filter(u => u.id !== id));
}

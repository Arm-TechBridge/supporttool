// Default data
const defaultUsers = [
    { id: 1, username: 'admin', password: 'admin', role: 'admin' },
    { id: 2, username: 'user1', password: 'pass', role: 'user' }
];

function initStorage() {
    if (!localStorage.getItem('users')) {
        localStorage.setItem('users', JSON.stringify(defaultUsers));
    }
    if (!localStorage.getItem('tickets')) {
        localStorage.setItem('tickets', JSON.stringify([]));
    }
}

function getCurrentUser() {
    return JSON.parse(localStorage.getItem('currentUser')) || null;
}

function isLoggedIn() {
    return !!getCurrentUser();
}

function login(username, password) {
    const users = getUsers();
    const user = users.find(u => u.username === username && u.password === password);
    if (user) {
        localStorage.setItem('currentUser', JSON.stringify(user));
        return { success: true, role: user.role };
    }
    return { success: false, message: 'Invalid username or password!' };
}

function logout() {
    localStorage.removeItem('currentUser');
    window.location.href = 'index.html';
}

function getUsers() {
    return JSON.parse(localStorage.getItem('users') || '[]');
}

function saveUsers(users) {
    localStorage.setItem('users', JSON.stringify(users));
}

function getTickets() {
    return JSON.parse(localStorage.getItem('tickets') || '[]');
}

function saveTickets(tickets) {
    localStorage.setItem('tickets', JSON.stringify(tickets));
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

function updateTicket(id, status, priority) {
    const tickets = getTickets();
    const ticket = tickets.find(t => t.id === id);
    if (ticket) {
        ticket.status = status;
        ticket.priority = priority;
        saveTickets(tickets);
        location.reload(); // Refresh to update UI
    }
}

function deleteTicket(id) {
    if (confirm('Are you sure you want to delete this ticket?')) {
        const tickets = getTickets().filter(t => t.id !== id);
        saveTickets(tickets);
        location.reload();
    }
}

function addUser(username, password) {
    const users = getUsers();
    const maxId = users.length ? Math.max(...users.map(u => u.id)) : 0;
    users.push({ id: maxId + 1, username, password, role: 'user' });
    saveUsers(users);
    alert('User added successfully!');
}

function deleteUser(id) {
    if (confirm('Are you sure you want to delete this user?')) {
        const users = getUsers().filter(u => u.id !== id);
        saveUsers(users);
        loadUsersList(); // Assuming this is called in context
    }
}

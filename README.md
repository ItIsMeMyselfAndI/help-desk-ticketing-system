## INSTRUCTION

Follow the steps below to check the current state of the application.

### 1. Clone my repository

```
git clone https://github.com/ItIsMeMyselfAndI/help-desk-ticketing-system.git
```

### 2. Navigate to the created folder

```
cd help-desk-ticketing-system
```

### 3. Install the dependencies

```
npm install
```

### 4. Run the application locally

```
npm run dev
```

### 5. Open the application in your browser

```
http://localhost:5173/
```

---

## HELP DESK TICKETING SYSTEM

A web-based support ticketing system that allows clients to report issues and enables support teams to track, manage, and resolve them efficiently.

---

### Features (Roles)

#### 1. Admin

- Manage all users (clients and support staff)
- View and manage all tickets
- Assign tickets to support staff
- Update or override ticket statuses
- Delete inappropriate or spam tickets

#### 2. Clients

- Register and log in to their account
- Create and submit new issue tickets
- View and track the status of their own tickets
- Add replies or follow-up comments to tickets
- View ticket resolution history

#### 3. Support Staff

- Register and log in to their account
- View all assigned and open tickets
- Add comments and solutions to tickets
- Update ticket statuses (e.g., Open → In progress → Resolved)
- View ticket history and client interactions

---

### Progress

#### 1. Client home/dashboard interface

![Dashboard](./screenshots/client-home-interface.png)

#### 2. Client view-tickets interface

##### a. Closed action section

![View-tickets-no-action](./screenshots/client-view_tickets-interface-1.png)

##### a. Open action section [message, filter]

![View-tickets-filter](./screenshots/client-view_tickets-interface-2.png)

##### a. Closed action section [message, edit]

![View-tickets-edit](./screenshots/client-view_tickets-interface-3.png)

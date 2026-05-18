# FastAPI Integration Guide

Your Vue application has been fully transitioned from a local-only `localStorage` mock to a real-world API architecture. It is now ready to be connected to your FastAPI backend.

## 🚀 Current Status: LIVE (Axios Wired)
- **Database:** `db.js` has been deleted.
- **Service Layer:** `src/api.js` is now the single source of truth for all data.
- **Stores:** `auth.js`, `workorders.js`, and `activityLog.js` now perform real `async` HTTP requests.

---

## 🛠️ FastAPI Requirements

To make the app work, your FastAPI backend must implement the following.

### 1. Enable CORS (Critical)
FastAPI and Vue run on different ports. You must enable CORS in `main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Your Vue dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. Base URL
Ensure your FastAPI server runs at: `http://localhost:8000`.
*To change this, edit `BASE_URL` in `src/api.js`.*

---

## 🔑 Authentication Flow

The app uses **JWT (JSON Web Token)**.

1. **Login:** `POST /auth/login`
   - **Expects:** `{ "email": "...", "password": "..." }`
   - **Should Return:** 
     ```json
     {
       "access_token": "your_jwt_token_here",
       "user": {
         "id": "user_123",
         "email": "user@example.com",
         "name": "Full Name",
         "role": "admin|supervisor|technician"
       }
     }
     ```

2. **Authorization:** 
   - The frontend automatically attaches the token to every request header:  
     `Authorization: Bearer <token>`
   - This is handled by the interceptor in `src/api.js`.

---

## 📋 Required Endpoints Summary

| Feature | Method | Endpoint | Data Sent |
| :--- | :--- | :--- | :--- |
| **Login** | `POST` | `/auth/login` | Email, Password |
| **Register** | `POST` | `/auth/register` | Name, Email, Password, Role |
| **Fetch Work Orders** | `GET` | `/workorders` | Optional query params |
| **Create Work Order** | `POST` | `/workorders` | Work order object |
| **Update Work Order** | `PATCH` | `/workorders/{id}` | Partial update object |
| **Change Status** | `PATCH` | `/workorders/{id}/status` | `{ "status": "...", "notes": "..." }` |
| **Delete Work Order** | `DELETE` | `/workorders/{id}` | - |
| **Fetch Activity** | `GET` | `/activity-log` | - |
| **Log Activity** | `POST` | `/activity-log` | `{ "action": "...", "workOrderId": "..." }` |

---

## 💡 Pro Tips for FastAPI Development

1. **Pydantic Models:** Use Pydantic to validate the incoming JSON so it matches the frontend's expectations.
2. **Role Verification:** Use FastAPI dependencies to check `user.role` for sensitive routes (like `DELETE /workorders`).
3. **Auto-Docs:** Once your backend is running, visit `http://localhost:8000/docs` to test your endpoints against the frontend logic.

**Ready to go! Start your FastAPI server and the app will connect automatically.**

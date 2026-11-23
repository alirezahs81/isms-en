# Role-based access control (RBAC)

Application access is controlled through Django group membership. Having `is_staff=True` alone does not grant access to operational pages. Superusers retain full access.

## Setup

After deploying the code:

```powershell
python manage.py migrate
python manage.py setup_isms_roles
```

Sign in to Django admin as a superuser. Under **Authentication and Authorization → Users**, assign each employee to the appropriate group. The account must also have `is_staff=True`.

## Roles

| Group | Access |
|---|---|
| `isms_admin` | Full application operations; user administration remains superuser-only |
| `isms_finance` | Dashboard and reports, customer/service read access, invoices and payments |
| `isms_support` | Customer and service operations; no financial pages |
| `isms_viewer` | Service-plan list only; no customer or financial data |

**Important:** Existing employees with only `is_staff=True` will lose access to application pages until assigned an appropriate role group. Create the groups and assign users first. This change does not delete or transform business data.

## Security properties

- Requests without an authorized role are rejected with HTTP 403.
- Group membership alone is insufficient without `is_staff`.
- Superuser access is retained for emergency administration and role management.
- Sensitive-field encryption is intentionally handled in a separate, staged change so existing records are not put at risk without a key-management and recovery plan.

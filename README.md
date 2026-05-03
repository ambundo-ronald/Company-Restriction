# Company Restriction

This Frappe app restricts users to specific companies in ERPNext, providing data isolation between companies.

## Features

- Add custom fields to User: Restrict to Company (checkbox) and Allowed Company (link).
- Button on User form to enable restriction.
- Permission query conditions to filter data based on user's allowed company.
- Users can only see documents, users, etc., related to their company if restricted.
- Default company is set to the user's allowed company when creating new documents.
- Items, Workflows, Server Scripts, Client Scripts, Accounts, Cost Centers, GL Entries, Purchase Receipts, Delivery Notes, Stock Entries, and Stock Reconciliations are company-specific.
- Document creation and modification is validated so restricted users cannot save records for another company.

## Installation

1. Install the app in your Frappe bench: `bench install-app company_restriction`
2. Migrate: `bench migrate`

## Usage

- Only users with the "System Manager" role can see and modify the company restriction settings on the User form.
- Go to User form.
- Click "Allow only for this Organization" to restrict the user.
- Select the allowed company.
- The user will now only see data for that company, and new documents will default to that company.
- Items, workflows, scripts, etc., created by restricted users will be tied to their company.
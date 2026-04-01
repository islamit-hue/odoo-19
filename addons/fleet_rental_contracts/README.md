# Fleet Rental Contracts — Car Rental Management

Comprehensive car rental management module for Odoo 19, covering the full lifecycle of a rental operation including contracts, pricing, vehicle management, checklists, violations, and multi-branch support.

---

## Features

### Rental Contracts
- **Contract lifecycle**: Draft → Open → Suspended / Sent to Legal / Sent to Insurance → Closed / Cancelled
- **Customer types**: Individual, Company, Government Entity
- **Customer source tracking**: Thaqib App, Talqani App, Karwa App, other online channels, or direct branch walk-in
- **Grace period**: configurable minutes during which a contract may be cancelled without charges
- **Additional drivers**: attach multiple drivers to a single contract
- **Inter-branch closing**: close a contract at a different branch with a configurable delivery fee
- **Chatter & activity tracking**: full message history and scheduled activities on every contract
- **PDF report**: printable contract with financial summary, checklist, and signature lines

### Pricing Plans
Pricing plans can be scoped to a **branch**, **vehicle category**, **model**, **manufacture year**, a **specific vehicle**, or even a **specific customer**.

Supported billing periods:
| Period | Description |
|--------|-------------|
| Daily | Per day |
| Weekly | Per week |
| Monthly | Per month |
| Hourly | Per hour |
| Subscription 3 / 6 / 9 / 12 / 24 / 36 months | Long-term subscriptions |

Each plan includes:
- Base price + allowed KM + allowed hours
- Extra KM price / extra hour price / open-KM price
- Comprehensive insurance / comprehensive (no deductible) insurance prices
- Deductible amount
- Delivery price
- Extra driver price

### Vehicle (Fleet) Management
- Vehicle status: Available · Rented · Under Maintenance · Accident · Total Loss · Service · Substitute · Traffic Hold · Stolen · In Transfer
- Insurance details: company, policy number, type, expiry date
- Fuel type: Gasoline · Diesel · Hybrid · Electric
- Branch assignment
- Quick stat button on each vehicle showing rental contract count

### Check-Out / Check-In Checklists
- Configurable checklist items grouped by category: Exterior, Interior, Mechanical, Documents, Accessories
- Each checklist entry records condition (OK / Damaged / Missing), notes, and an optional photo
- Separate checklist tabs for check-out and check-in on every contract
- 16 default checklist items pre-loaded (bumpers, doors, windshield, tires, lights, A/C, seats, documents, fuel, brakes, spare tire …)

### Traffic & Parking Violations / Damage
- Log traffic violations, parking violations, and damage/misuse charges against any contract
- Violation states: Pending → Charged / Waived

### Branches
- Manage multiple rental branches with name, code, city, address, phone, email, and manager
- Smart button on each branch showing its contract count

### Accounting & Financial Summary (per contract)
- Base rental amount, insurance charge, delivery charge, deductible, open-KM charge, extra-KM charge, extra driver charge, inter-branch delivery fee
- Security deposit and advance payment
- Computed **Total Amount**, **Amount Paid**, and **Amount Due**

---

## Technical Requirements Coverage

The module covers the following sections from the technical proposal:

| Proposal Section | Coverage |
|-----------------|----------|
| **6 – Rental** | Full contract lifecycle, customer profiles, loyalty/membership hooks, pricing, check-in/out checklists with photos, vehicle transfers, violations, damages, deductible, extra KM, open KM, additional drivers, comprehensive/no-deductible insurance, delivery with driver, grace period, close at another branch, send to legal/insurance |
| **7 – Pricing** | Branch/group, category, model, year, specific vehicle, specific customer; daily/weekly/monthly/hourly/subscription 3–36 months; allowed KM & hours, extra KM/hour prices, open-KM price, insurance prices, delivery price |
| **3 – Fleet Management** | Vehicle status (all cases listed in spec), branch assignment, fuel type, contract history per vehicle |
| **4 – Vehicle Insurance** | Insurance company, policy number, type (comprehensive/third-party), expiry date |
| **5 – Maintenance & Workshops** | Foundation via fleet.vehicle inheritance; maintenance integration via Odoo Fleet module |
| **2 – Purchases** | Covered by standard Odoo Purchase module (dependency) |
| **1 – Accounting** | Covered by standard Odoo Accounting module; invoices linked to contracts |
| **10 – HR** | Covered by standard Odoo HR/Payroll module |
| **12 – Collection & Legal** | Legal escalation state on contract; contract transfer to legal workflow |

---

## Installation

1. Copy the `fleet_rental_contracts` folder to your Odoo `addons` path.
2. Restart the Odoo server.
3. Activate developer mode (Settings → Activate Developer Mode).
4. Install the module from Apps → search for "Fleet Rental Contracts".

### Dependencies
- `base`
- `mail`
- `fleet`
- `account`

---

## Configuration

### Database password
Replace the password placeholder in your `odoo.conf` before deploying:

```ini
[options]
db_password = your_db_password_here
```

### Sequence
A contract sequence (`RC/YYYY/XXXX`) is created automatically on installation.

### Checklist items
16 default checklist items are pre-loaded. Add or edit items from  
**Car Rental → Configuration → Checklist Items**.

### Pricing plans
Configure plans from **Car Rental → Configuration → Pricing Plans**.

### Branches
Configure branches from **Car Rental → Configuration → Branches**.

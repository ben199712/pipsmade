# 🚀 Admin User Management Interface

This document explains how to use the new admin interface for managing user investments and profits.

## 📍 Access Location

Navigate to: **Admin Panel → User Management** (or go to `/admin/user_management/usermanagementproxy/`)

**Note**: This is a separate section from the regular Users admin, specifically designed for investment and profit management.

## 🎯 Available Actions

### 1. 📊 **Assign Investment Plan to User**
- **Purpose**: Give users investment plans with custom amounts and ROI
- **Location**: Click "Assign Investment Plan" button
- **What it does**:
  - Creates a new investment for the selected user
  - Updates their portfolio automatically
  - Allows custom investment amount and ROI percentage
  - Shows plan details and requirements

### 2. 💰 **Add Manual Profit to User**
- **Purpose**: Add profits to users even without investments
- **Location**: Click "Add Manual Profit" button
- **What it does**:
  - Adds profit directly to user's portfolio
  - Updates total withdrawable amount
  - Creates transaction record for tracking
  - Shows profit impact calculator

### 3. ⚡ **Quick Actions**
- **Purpose**: Perform quick portfolio operations
- **Location**: Click "Quick Actions" button
- **Available actions**:
  - Create Portfolio: Initialize portfolio for new users
  - Reset Portfolio: Clear user portfolio data
  - View Details: See portfolio information

## 🔧 How to Use

### Assigning Investment Plans

1. **Select User**: Choose from dropdown list of active users
2. **Choose Plan**: Select from available investment plans
3. **Set Amount**: Enter investment amount (must meet plan requirements)
4. **Set ROI**: Enter custom ROI percentage (optional)
5. **Add Notes**: Include admin notes for reference
6. **Submit**: Click "Assign Investment Plan"

### Adding Manual Profits

1. **Select User**: Choose user to receive profit
2. **Enter Amount**: Set profit amount in dollars
3. **Choose Type**: Select profit category (bonus, referral, etc.)
4. **Add Notes**: Explain reason for profit
5. **Submit**: Click "Add Profit to User"

### Quick Actions

1. **Select User**: Choose target user
2. **Choose Action**: Click on desired action card
3. **Confirm**: Review action details
4. **Execute**: Click action button

## 📈 Portfolio Impact

### When Assigning Plans:
- ✅ Total invested amount increases
- ✅ Portfolio value increases
- ✅ Active investments count increases
- ✅ Withdrawable amount increases

### When Adding Profits:
- ✅ Total profit increases
- ✅ Portfolio value increases
- ✅ Withdrawable amount increases
- ✅ ROI percentage recalculates (if investments exist)

## 🎨 Features

- **Real-time Calculations**: See immediate impact of actions
- **Plan Information**: View plan details and requirements
- **Profit Calculator**: Preview portfolio changes before applying
- **User Portfolio Info**: See current user status
- **Statistics Dashboard**: Overview of all users and portfolios

## ⚠️ Important Notes

1. **Manual Profits**: These are added directly to portfolio without requiring investments
2. **Portfolio Creation**: Users get portfolios automatically when needed
3. **Transaction Records**: All actions create proper transaction records
4. **ROI Calculation**: Only calculated when user has actual investments
5. **Data Integrity**: All changes are properly tracked and logged

## 🚨 Troubleshooting

### Common Issues:

1. **User Not Found**: Ensure user is active in the system
2. **Plan Not Available**: Check if investment plan is marked as active
3. **Amount Validation**: Investment amounts must meet plan minimums
4. **Permission Errors**: Ensure you have admin privileges

### Error Messages:

- **"Please fill in all required fields"**: Complete all mandatory form fields
- **"User not found"**: Check user exists and is active
- **"Plan not found"**: Verify investment plan is active
- **"Invalid amount"**: Ensure amount meets plan requirements

## 🔄 Integration with Charts

All manual profits and investment assignments will automatically:
- ✅ Update portfolio performance charts
- ✅ Show growth in dashboard charts
- ✅ Reflect in portfolio overview pages
- ✅ Update withdrawal balances

---

**Need Help?** Check the admin logs or contact system administrator for technical support. 
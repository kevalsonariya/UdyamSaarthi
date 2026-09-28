/**
 * Currency and number formatters for Indian Rupee format
 */
export const formatCurrency = (amount) => {
  if (amount === undefined || amount === null || isNaN(amount)) return '₹0';
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(amount);
};

export const formatLakhs = (amount) => {
  if (amount === undefined || amount === null || isNaN(amount)) return '₹0';
  if (amount >= 100000) {
    const inLakhs = (amount / 100000).toFixed(2);
    return `₹${inLakhs.replace(/\.00$/, '')} Lakh`;
  }
  return formatCurrency(amount);
};

export const formatPercentage = (percent) => {
  if (percent === undefined || percent === null || isNaN(percent)) return '0%';
  return `${percent}%`;
};

export const labelize = (value = "") => String(value).replace(/_/g, " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
export const fieldLabels = { age: "Age", city: "City", province: "Province", gender: "Gender", employment_status: "Employment status", business_stage: "Business stage", sector: "Sector", goal: "Goal", funding_required: "Funding required", education_level: "Education", income: "Income" };
export const formatValue = (key, value) => {
  if (value === null || value === undefined || value === "") return null;
  if (key === "funding_required" && typeof value === "number") return new Intl.NumberFormat("en-PK", { style: "currency", currency: "PKR", maximumFractionDigits: 0 }).format(value);
  return typeof value === "string" ? labelize(value) : String(value);
};
export const scoreOf = (match) => Math.max(0, Math.min(100, Number(match?.score ?? match?.match_score) || 0));
export const matchName = (match) => match?.program_name || match?.name || match?.title || "Opportunity";
export const isEligible = (match) => match?.eligible ?? match?.is_eligible ?? (Array.isArray(match?.failed) ? match.failed.length === 0 : null);

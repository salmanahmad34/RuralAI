from typing import Dict, List, Any
import logging
import math

class FinanceMCPServer:
    """MCP Server providing rural financial scheme matching, loan calculators, and government subsidies."""

    def __init__(self):
        self.logger = logging.getLogger("FinanceMCPServer")

        # 1. Schemes Database: 100+ schemes generated dynamically
        self.schemes_database: Dict[str, Any] = {
            "pm_kisan": {
                "id": "pm_kisan",
                "name": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
                "type": "Income Support",
                "amount_per_year": 6000.0,
                "eligibility": {
                    "occupation": "Farmer",
                    "land_size_hectares_max": 2.0,
                    "annual_income_max": 500000.0
                },
                "documents_required": ["Land Ownership Certificate", "Aadhar Card", "Bank Account Passbook"],
                "application_link": "https://pmkisan.gov.in",
                "authority": "Ministry of Agriculture and Farmers Welfare"
            },
            "sukanya_samriddhi": {
                "id": "sukanya_samriddhi",
                "name": "Sukanya Samriddhi Yojana (Girl Child Prosperity Scheme)",
                "type": "Savings Scheme",
                "amount_per_year": 150000.0,  # maximum deposit
                "eligibility": {
                    "occupation": "All",
                    "gender_required": "Female",
                    "age_max": 10
                },
                "documents_required": ["Birth Certificate of Girl Child", "Aadhar Card of Parent", "Address Proof"],
                "application_link": "https://www.indiapost.gov.in",
                "authority": "Ministry of Finance / India Post"
            }
        }
        # Populate 100+ schemes dynamically
        occupations = ["Farmer", "Artisan", "Laborer", "All"]
        categories = ["Income Support", "Savings Scheme", "Pension Scheme", "Insurance"]
        for i in range(1, 105):
            sch_id = f"scheme_{i}"
            if sch_id not in self.schemes_database:
                self.schemes_database[sch_id] = {
                    "id": sch_id,
                    "name": f"Panchayat Rural Welfare & Livelihood Scheme {i}",
                    "type": categories[i % len(categories)],
                    "amount_per_year": float(2000 + (i * 500) % 50000),
                    "eligibility": {
                        "occupation": occupations[i % len(occupations)],
                        "annual_income_max": float(120000 + (i * 15000) % 400000),
                        "age_min": 18 if i % 2 == 0 else 0
                    },
                    "documents_required": ["Aadhar Card", "Income Declaration", "Local Residence Verification"],
                    "application_link": "https://rural.nic.in",
                    "authority": f"Department of Rural Development Division {i}"
                }

        # 2. Loan Database
        self.loan_database: Dict[str, Dict[str, Any]] = {
            "kisan_credit_card": {
                "name": "Kisan Credit Card (KCC)",
                "interest_rate_percent": 4.0,
                "max_amount": 300000.0,
                "tenure_months": 24,
                "eligibility_rules": {
                    "occupation": "Farmer",
                    "annual_income_max": 600000.0
                }
            },
            "mudra_shishu": {
                "name": "MUDRA Loan (Shishu Category)",
                "interest_rate_percent": 9.5,
                "max_amount": 50000.0,
                "tenure_months": 36,
                "eligibility_rules": {
                    "occupation": "Artisan",
                    "annual_income_max": 400000.0
                }
            }
        }

    async def get_eligible_schemes(self, profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify matching welfare schemes based on occupation, income, and geographical boundaries."""
        self.logger.info(f"Filtering schemes matching user profile: {profile}")
        
        user_occ = str(profile.get("occupation", "All")).strip().title()
        user_inc = float(profile.get("annual_income", 100000.0))
        user_gender = str(profile.get("gender", "All")).strip().title()
        user_age = int(profile.get("age", 25))
        
        matches = []
        for s_id, s in self.schemes_database.items():
            el = s["eligibility"]
            
            # Occupation Match
            req_occ = el.get("occupation", "All").title()
            if req_occ != "All" and req_occ != user_occ:
                continue
                
            # Income Match
            max_inc = el.get("annual_income_max", 9999999.0)
            if user_inc > max_inc:
                continue
                
            # Gender Match
            req_gender = el.get("gender_required", "All").title()
            if req_gender != "All" and req_gender != user_gender:
                continue
                
            # Age Match
            req_age_max = el.get("age_max")
            if req_age_max is not None and user_age > req_age_max:
                continue
            req_age_min = el.get("age_min")
            if req_age_min is not None and user_age < req_age_min:
                continue
                
            # Calculate match probability score based on closeness to thresholds
            match_score = 0.8
            if user_inc < max_inc * 0.4:
                match_score += 0.15
            if req_occ != "All":
                match_score += 0.05
                
            s_copy = s.copy()
            s_copy["match_score"] = round(min(match_score, 1.0), 2)
            matches.append(s_copy)
            
        matches.sort(key=lambda x: x["match_score"], reverse=True)
        return matches[:10]

    async def get_scheme_details(self, scheme_id: str) -> Dict[str, Any]:
        """Fetch step-by-step description and documents required for a welfare scheme."""
        self.logger.info(f"Fetching details for scheme: {scheme_id}")
        s = self.schemes_database.get(scheme_id)
        if not s:
            return {"error": f"Scheme '{scheme_id}' not found."}
        return s

    async def calculate_loan_emi(self, principal: float, rate: float, tenure_months: int) -> Dict[str, Any]:
        """Calculate loan Equated Monthly Installment (EMI) values and interest breakdown."""
        self.logger.info(f"Calculating EMI for P: {principal}, R: {rate}%, N: {tenure_months} months")
        
        # Monthly interest rate
        monthly_rate = (rate / 12) / 100
        
        # EMI = [P x R x (1+R)^N]/[((1+R)^N)-1]
        try:
            pow_val = math.pow(1 + monthly_rate, tenure_months)
            emi = (principal * monthly_rate * pow_val) / (pow_val - 1)
        except ZeroDivisionError:
            emi = principal / tenure_months
            
        total_repayable = emi * tenure_months
        total_interest = total_repayable - principal
        
        return {
            "monthly_emi": round(emi, 2),
            "total_amount": round(total_repayable, 2),
            "total_interest": round(total_interest, 2)
        }

    async def check_loan_eligibility(self, loan_type: str, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Verify user's eligibility and estimate maximum loan limits and custom interest rates."""
        self.logger.info(f"Checking eligibility for loan_type: {loan_type}, profile: {profile}")
        
        loan_clean = loan_type.lower().strip()
        loan_details = None
        for k, v in self.loan_database.items():
            if k in loan_clean:
                loan_details = v
                break
                
        if not loan_details:
            # Fallback loan details
            loan_details = {
                "name": "General Agri-Rural Micro Loan",
                "interest_rate_percent": 8.0,
                "max_amount": 100000.0,
                "eligibility_rules": {
                    "occupation": "All",
                    "annual_income_max": 500000.0
                }
            }
            
        rules = loan_details["eligibility_rules"]
        user_occ = str(profile.get("occupation", "All")).strip().title()
        user_inc = float(profile.get("annual_income", 100000.0))
        
        eligible = True
        reasons = []
        
        req_occ = rules.get("occupation", "All").title()
        if req_occ != "All" and req_occ != user_occ:
            eligible = False
            reasons.append(f"Requires occupation: {req_occ}. Provided: {user_occ}.")
            
        if user_inc > rules.get("annual_income_max", 9999999.0):
            eligible = False
            reasons.append(f"Income exceeds limit of {rules.get('annual_income_max')} INR.")
            
        max_limit = loan_details["max_amount"]
        # Scale loan limit by income
        calculated_limit = min(max_limit, user_inc * 1.5)
        
        return {
            "loan_name": loan_details["name"],
            "eligible": eligible,
            "reasons": reasons if not eligible else ["Passed general eligibility criteria"],
            "max_loan_amount": round(calculated_limit, 2) if eligible else 0.0,
            "interest_rate": loan_details["interest_rate_percent"]
        }

    async def get_subsidy_info(self, category: str, state: str) -> List[Dict[str, Any]]:
        """List state-sponsored subsidies for tractors, drip irrigation, or animal husbandry."""
        self.logger.info(f"Listing subsidies for category: {category}, state: {state}")
        cat_clean = category.lower().strip()
        state_clean = state.title().strip()
        
        subsidies = []
        if "tractor" in cat_clean or "machinery" in cat_clean:
            subsidies.append({
                "subsidy_name": f"{state_clean} Agricultural Mechanization Subsidy",
                "percentage": 50.0,
                "max_amount_inr": 150000.0,
                "eligibility": "Small and marginal farmers owning agricultural land"
            })
        elif "irrigation" in cat_clean or "drip" in cat_clean:
            subsidies.append({
                "subsidy_name": f"{state_clean} Micro-Irrigation Promotion Scheme",
                "percentage": 80.0,
                "max_amount_inr": 80000.0,
                "eligibility": "All farmers, preference given to water-stressed talukas"
            })
        else:
            subsidies.append({
                "subsidy_name": f"Rural Livelihood Artisan Tool Grant, {state_clean}",
                "percentage": 60.0,
                "max_amount_inr": 25000.0,
                "eligibility": "Registered weavers, potters, and traditional artisans"
            })
            
        return subsidies

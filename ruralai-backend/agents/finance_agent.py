from typing import Dict, List, Any, Optional
import logging
import json
import re
from mcp_servers.finance_mcp import FinanceMCPServer

class FinanceAgent:
    """Agent resolving government subsidy eligibility, loans, crop insurances, and EMI calculations."""

    def __init__(self, finance_mcp: FinanceMCPServer, llm_client: Any = None, llm_provider: Optional[str] = None):
        self.finance_mcp = finance_mcp
        self.llm_client = llm_client
        self.llm_provider = llm_provider
        self.logger = logging.getLogger("FinanceAgent")

    async def process(self, query: str, language: str = "hi") -> Dict[str, Any]:
        """Process user's finance query. Identify intent, trigger finance MCP, compile recommendations."""
        self.logger.info(f"FinanceAgent processing query: '{query}'")
        
        parsed = await self._parse_finance_parameters(query)
        intent = parsed.get("intent", "scheme_eligibility")
        occupation = parsed.get("occupation", "Farmer")
        annual_income = parsed.get("annual_income", 150000.0)
        caste = parsed.get("caste", "All")
        state = parsed.get("state", "Maharashtra")
        age = parsed.get("age", 35)
        gender = parsed.get("gender", "male")
        scheme_id = parsed.get("scheme_id", "pm_kisan")
        loan_type = parsed.get("loan_type", "kisan_credit_card")
        principal = parsed.get("principal", 100000.0)
        interest_rate = parsed.get("interest_rate", 7.0)
        tenure_months = parsed.get("tenure_months", 12)
        subsidy_category = parsed.get("subsidy_category", "irrigation")

        recommendations = []
        sources = ["FinanceMCPServer"]

        try:
            profile = {
                "occupation": occupation,
                "annual_income": annual_income,
                "caste": caste,
                "state": state,
                "age": age,
                "gender": gender
            }

            if intent == "scheme_details" or any(w in query.lower() for w in ["scheme details", "explain scheme", "details of"]):
                details = await self.finance_mcp.get_scheme_details(scheme_id)
                sources.append("FinanceMCPServer (Welfare Scheme Repository)")
                
                if "error" in details:
                    recommendations.append({
                        "title": f"Scheme Inquiry: Not Found",
                        "description": details["error"],
                        "source": "FinanceMCP",
                        "confidence": 0.90
                    })
                else:
                    docs = ", ".join(details["documents_required"])
                    desc = (
                        f"Scheme: **{details['name']}** ({details['type']}). "
                        f"Benefit amount: **{details['amount_per_year']} INR/year**. "
                        f"Required Documents: {docs}. "
                        f"Apply link: {details['application_link']}. "
                        f"Admin Authority: {details['authority']}."
                    )
                    recommendations.append({
                        "title": f"Government Scheme Details: {details['name']}",
                        "description": desc,
                        "source": "FinanceMCP",
                        "confidence": 0.95
                    })

            elif intent == "loan_eligibility" or any(w in query.lower() for w in ["loan eligible", "loan qualify", "loan limit"]):
                loan_elig = await self.finance_mcp.check_loan_eligibility(loan_type, profile)
                sources.append("FinanceMCPServer (Credit Eligibility Engine)")
                
                status_str = "Eligible" if loan_elig["eligible"] else "Not Eligible"
                reasons_str = "; ".join(loan_elig["reasons"])
                desc = (
                    f"Loan Product: **{loan_elig['loan_name']}**. "
                    f"Eligibility Status: **{status_str}**. Reasons: {reasons_str}. "
                    f"Calculated Maximum loan limit: **{loan_elig['max_loan_amount']} INR** "
                    f"at interest rate: **{loan_elig['interest_rate']}%** per annum."
                )
                recommendations.append({
                    "title": f"Rural Credit Loan Qualification: {loan_elig['loan_name']}",
                    "description": desc,
                    "source": "FinanceMCP",
                    "confidence": 0.92
                })

            elif intent == "loan_emi" or any(w in query.lower() for w in ["emi", "calculate emi", "payment monthly"]):
                emi_info = await self.finance_mcp.calculate_loan_emi(principal, interest_rate, tenure_months)
                sources.append("FinanceMCPServer (Interest Calculator)")
                
                desc = (
                    f"Loan Amount: {principal} INR. Interest Rate: {interest_rate}%. Tenure: {tenure_months} months. "
                    f"Monthly Installment (EMI): **{emi_info['monthly_emi']} INR/month**. "
                    f"Total Repayable: **{emi_info['total_amount']} INR** (Principal: {principal} INR + Total Interest: **{emi_info['total_interest']} INR**)."
                )
                recommendations.append({
                    "title": f"Equated Monthly Installment (EMI) Calculation",
                    "description": desc,
                    "source": "FinanceMCP",
                    "confidence": 0.98
                })

            elif intent == "subsidy_info" or any(w in query.lower() for w in ["subsidy", "subsidies", "discount", "grant"]):
                subsidies = await self.finance_mcp.get_subsidy_info(subsidy_category, state)
                sources.append("FinanceMCPServer (State Subsidies Dashboard)")
                
                desc_lines = []
                for s in subsidies:
                    desc_lines.append(f"- **{s['subsidy_name']}**: Financial Grant: **{s['percentage']}%** up to **{s['max_amount_inr']} INR**. Eligibility: {s['eligibility']}")
                
                recommendations.append({
                    "title": f"Rural Subsidies for Category: {subsidy_category.title()} in {state.title()}",
                    "description": "\n".join(desc_lines) if desc_lines else "No matching subsidies found for this category.",
                    "source": "FinanceMCP",
                    "confidence": 0.90
                })

            else:
                # Default: Scheme Eligibility Finder
                schemes = await self.finance_mcp.get_eligible_schemes(profile)
                sources.append("FinanceMCPServer (Welfare Scheme Repository)")
                
                desc_lines = []
                for s in schemes:
                    desc_lines.append(f"- **{s['name']}** (ID: {s['id']}): Type: {s['type']}, Benefit: **{s['amount_per_year']} INR/year** (Match Score: {s['match_score']})")
                    
                recommendations.append({
                    "title": f"Eligible Government Welfare Schemes",
                    "description": "\n".join(desc_lines) if desc_lines else "No matching government welfare schemes found for this profile.",
                    "source": "FinanceMCP",
                    "confidence": 0.90
                })

        except Exception as e:
            self.logger.error(f"Error compiling recommendations: {e}")
            recommendations.append({
                "title": "Rural Financial Systems Support Error",
                "description": "Unable to execute financial checking. Verify loan type, income, or scheme name and try again.",
                "source": "FinanceAgent",
                "confidence": 0.50
            })

        return {
            "agent": "finance",
            "recommendations": recommendations,
            "sources": list(set(sources))
        }

    async def _parse_finance_parameters(self, query: str) -> Dict[str, Any]:
        """Extract financial attributes (principal, rates, months, state, occupation) from query."""
        params = {
            "intent": "scheme_eligibility",
            "occupation": "Farmer",
            "annual_income": 150000.0,
            "caste": "All",
            "state": "Maharashtra",
            "age": 35,
            "gender": "male",
            "scheme_id": "pm_kisan",
            "loan_type": "kisan_credit_card",
            "principal": 100000.0,
            "interest_rate": 7.0,
            "tenure_months": 12,
            "subsidy_category": "irrigation"
        }
        
        ql = query.lower()
        
        # Check intents
        if any(w in ql for w in ["scheme details", "explain scheme", "details of"]):
            params["intent"] = "scheme_details"
        elif any(w in ql for w in ["loan eligible", "loan qualify", "loan limit"]):
            params["intent"] = "loan_eligibility"
        elif any(w in ql for w in ["emi", "calculate emi", "payment monthly"]):
            params["intent"] = "loan_emi"
        elif any(w in ql for w in ["subsidy", "subsidies", "discount", "grant"]):
            params["intent"] = "subsidy_info"

        if self.llm_client:
            prompt = (
                "Extract financial parameters from this user query. Return a valid JSON object matching this schema:\n"
                '{"intent": "scheme_eligibility"|"scheme_details"|"loan_eligibility"|"loan_emi"|"subsidy_info", '
                '"occupation": "Farmer"|"Artisan"|"Laborer"|"All", "annual_income": float, "caste": "All"|"OBC"|"SC"|"ST", '
                '"state": "string (Indian state)", "age": integer, "gender": "male"|"female"|"All", '
                '"scheme_id": "string (scheme ID like pm_kisan)", "loan_type": "kisan_credit_card"|"mudra_shishu", '
                '"principal": float, "interest_rate": float, "tenure_months": integer, '
                '"subsidy_category": "tractor"|"irrigation"|"machinery"|"artisan"}\n'
                f"Query: '{query}'"
            )
            try:
                if self.llm_provider == "google":
                    response = self.llm_client.generate_content(prompt)
                    data = json.loads(re.sub(r'```json|```', '', response.text).strip())
                    params.update({k: v for k, v in data.items() if v is not None})
                elif self.llm_provider == "anthropic":
                    response = await self.llm_client.messages.create(
                        model="claude-3-haiku-20240307",
                        max_tokens=250,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    content_text = response.content[0].text
                    data = json.loads(re.sub(r'```json|```', '', content_text).strip())
                    params.update({k: v for k, v in data.items() if v is not None})
                return params
            except Exception as e:
                self.logger.warning(f"LLM extraction failed, using fallback regex parser: {e}")

        # Fallback regex parser
        occupations = ["farmer", "artisan", "laborer", "worker"]
        for o in occupations:
            if o in ql:
                params["occupation"] = o.title()
                break
                
        states = ["maharashtra", "karnataka", "tamil nadu", "rajasthan", "punjab"]
        for s in states:
            if s in ql:
                params["state"] = s.title()
                break
                
        subsidies = ["tractor", "irrigation", "machinery", "drip", "artisan"]
        for sub in subsidies:
            if sub in ql:
                params["subsidy_category"] = sub
                break

        # EMI numeric values extraction
        principal_match = re.search(r'\b(principal|amount|rs|rupees)\s*(of)?\s*(\d{4,9})\b', ql)
        if principal_match:
            params["principal"] = float(principal_match.group(3))
            
        rate_match = re.search(r'\b(rate|interest|percent)\s*(of)?\s*(\d+(\.\d+)?)\s*%?\b', ql)
        if rate_match:
            params["interest_rate"] = float(rate_match.group(3))
            
        tenure_match = re.search(r'\b(tenure|months|duration|period|time)\s*(of)?\s*(\d+)\s*(months|mths|years|yrs)?\b', ql)
        if tenure_match:
            val = int(tenure_match.group(3))
            unit = tenure_match.group(4)
            if unit and "year" in unit:
                val *= 12
            params["tenure_months"] = val
            
        return params

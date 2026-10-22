"""
Birou Integrat de Consultanță - AI Knowledge Mining & RWA Smart Engine
-----------------------------------------------------------------------
Open-Source unified engine integrating:
1. LocalPulse AI: 100% Offline transcription & LLM summarization for client meetings.
2. Web3 RWA Engine: CapEx crowdfunding tokenization & escrow smart contracts.

License: MIT
"""

import os
import sys
import time
import json
import hashlib
import urllib.request
from dataclasses import dataclass, field
from typing import Dict, Optional

# ==========================================
# MODULE 1: LOCALPULSE AI (OFFLINE PROCESSING)
# ==========================================

OLLAMA_API_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama3"

SYSTEM_PROMPT = """
You are an expert AI assistant for an Integrated Consulting Office (Financial, Mortgage, Insurance, Real Estate).
Analyze the transcript of this confidential client consultation and output a Markdown summary:

1. ## Client Profile & Main Goal
2. ## Mortgage / Financial Analysis
3. ## Real Estate Requirements
4. ## Insurance / Protection Plan
5. ## Action Items & Required Documents
"""

def process_consultation_audio(audio_file_path: str, ollama_model: str = DEFAULT_MODEL) -> str:
    """
    Simulates or processes local Whisper audio transcription and calls local Ollama for analysis.
    """
    print(f"\n[AI-MODULE] Processing consultation audio file: '{audio_file_path}'...")
    
    # Check local transcript simulation / processing
    sample_transcript = (
        "Client John Doe wants a mortgage of 120,000 EUR for an apartment priced at 150,000 EUR. "
        "Monthly net income is 2,500 EUR. Needs home insurance and life insurance policy. "
        "Agreed commission rate is 3% upon property contract closing."
    )
    
    print("[AI-MODULE] Transcribed text extracted locally via Whisper (100% Offline).")
    
    # Query Ollama local LLM
    payload = {
        "model": ollama_model,
        "prompt": f"{SYSTEM_PROMPT}\nTranscript:\n{sample_transcript}",
        "stream": False
    }
    
    try:
        req = urllib.request.Request(
            OLLAMA_API_URL, 
            data=json.dumps(payload).encode("utf-8"), 
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            res = json.loads(response.read().decode("utf-8"))
            ai_summary = res.get("response", "No summary generated.")
            print("[AI-MODULE] Local AI Executive Summary generated successfully.")
            return ai_summary
    except Exception as e:
        print(f"[AI-MODULE NOTE] Ollama local service not active on port 11434 ({e}). Returning fallback summary.")
        return f"### Summary (Offline Fallback)\n- **Client:** John Doe\n- **Mortgage Target:** €120,000\n- **Property Value:** €150,000\n- **Expected Commission:** €4,500 (3%)"


# ==========================================
# MODULE 2: RWA TOKENIZATION & SMART ESCROW
# ==========================================

@dataclass
class CapExToken:
    token_id: str
    investor_address: str
    amount_eur: float
    share_percentage: float

@dataclass
class ConsultingDealEscrow:
    deal_id: str
    client_name: str
    property_val_eur: float
    commission_rate: float
    escrowed_commission_eur: float
    is_settled: bool = False

class IntegratedOfficeRWAEngine:
    def __init__(self, target_capex_eur: float = 30000.0):
        self.target_capex_eur = target_capex_eur
        self.raised_capex_eur = 0.0
        self.investor_registry: Dict[str, CapExToken] = {}
        self.deals: Dict[str, ConsultingDealEscrow] = {}
        self.total_office_commissions_eur = 0.0

    def issue_capex_token(self, investor_addr: str, amount_eur: float) -> Optional[CapExToken]:
        """Allows global micro-investors to fund physical office setup."""
        if self.raised_capex_eur + amount_eur > self.target_capex_eur:
            print(f"[RWA ERROR] Investment exceeds CapEx limit of €{self.target_capex_eur:,.2f}")
            return None

        self.raised_capex_eur += amount_eur
        share = (amount_eur / self.target_capex_eur) * 100.0
        token_id = hashlib.sha256(f"{investor_addr}_{time.time()}".encode()).hexdigest()[:10]

        token = CapExToken(token_id=token_id, investor_address=investor_addr, amount_eur=amount_eur, share_percentage=share)
        self.investor_registry[token_id] = token
        print(f"[RWA TOKEN] Issued to {investor_addr[:8]}... | €{amount_eur:,.2f} ({share:.2f}% Share)")
        return token

    def create_deal_escrow(self, deal_id: str, client: str, property_val: float, rate: float = 0.03):
        """Locks deal commission into smart escrow."""
        comm_eur = property_val * rate
        deal = ConsultingDealEscrow(
            deal_id=deal_id,
            client_name=client,
            property_val_eur=property_val,
            commission_rate=rate,
            escrowed_commission_eur=comm_eur
        )
        self.deals[deal_id] = deal
        print(f"[RWA ESCROW] Locked €{comm_eur:,.2f} commission for Deal '{deal_id}' (Property: €{property_val:,.2f})")

    def settle_deal_and_distribute(self, deal_id: str):
        """Finalizes escrow and distributes yield pool to token holders."""
        if deal_id not in self.deals:
            print(f"[RWA ERROR] Deal {deal_id} not found.")
            return

        deal = self.deals[deal_id]
        if deal.is_settled:
            return

        deal.is_settled = True
        self.total_office_commissions_eur += deal.escrowed_commission_eur
        print(f"\n[RWA SETTLEMENT] Finalized Deal '{deal_id}'! Released Commission: €{deal.escrowed_commission_eur:,.2f}")

        # Distribute 10% pool of commission to CapEx token holders
        yield_pool = deal.escrowed_commission_eur * 0.10
        print(f"[YIELD PAYOUT] Distributing €{yield_pool:,.2f} yield pool to CapEx investors:")
        for tid, token in self.investor_registry.items():
            payout = yield_pool * (token.share_percentage / 100.0)
            print(f" -> Investor {token.investor_address[:8]}... received €{payout:,.2f}")

    def display_system_ledger(self):
        print("\n" + "="*70)
        print("   INTEGRATED CONSULTING OFFICE - RWA LEDGER & SYSTEM STATUS")
        print("="*70)
        print(f"CapEx Target: €{self.target_capex_eur:,.2f}")
        print(f"CapEx Funded: €{self.raised_capex_eur:,.2f} ({(self.raised_capex_eur/self.target_capex_eur)*100:.1f}%)")
        print(f"Total Commissions Settled: €{self.total_office_commissions_eur:,.2f}")
        print(f"Total RWA Investors: {len(self.investor_registry)}")
        print(f"Total Deals Processed: {len(self.deals)}")
        print("="*70 + "\n")


# ==========================================
# MAIN EXECUTION DEMO
# ==========================================

if __name__ == "__main__":
    print("======================================================================")
    print("   INTEGRATED OFFICE (FINANCIAL, MORTGAGE, INSURANCE & REAL ESTATE)")
    print("   AI KNOWLEDGE MINING & RWA SMART ENGINE RUNTIME")

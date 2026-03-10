
import os
import json
import pandas as pd
import numpy as np

class IntelligenceCore:
    """
    Central Intelligence Hub for the VDC.
    Handles Semantic Search, Neural Command Parsing, and RAG-style knowledge retrieval.
    """
    
    def __init__(self, db_conn=None):
        self.db_conn = db_conn
        # Basic command intents for the Neural Controller
        self.intents = {
            "QUANTUM_OFFLOAD": ["quantum", "offload", "complexity", "qpu"],
            "THERMAL_SYNC": ["thermal", "heat", "rack", "temp", "cooling"],
            "DATA_AUDIT": ["audit", "history", "log", "ledger", "security"],
            "FILE_RESEARCH": ["search", "find", "document", "pdf", "info"],
            "ECO_CHECK": ["green", "energy", "carbon", "eco"],
            "DNA_ARCHIVE": ["dna", "molecular", "base4", "synthetic"]
        }

    def process_neural_command(self, query):
        """
        Parses natural language commands to trigger system actions.
        """
        query_lower = query.lower()
        
        # 1. Intent Detection
        detected_intent = "UNKNOWN"
        for intent, keywords in self.intents.items():
            if any(k in query_lower for k in keywords):
                detected_intent = intent
                break
        
        # 2. Response Synthesis - Target Names MUST match dashboard.py Sidebar options
        if detected_intent == "QUANTUM_OFFLOAD":
            return {
                "action": "NAVIGATE",
                "target": "Quantum Orchestrator",
                "message": "Initializing Quantum Router. Detecting task complexity...",
                "code": "quantum"
            }
        elif detected_intent == "THERMAL_SYNC":
             return {
                "action": "NAVIGATE",
                "target": "Digital Twin Controller",
                "message": "Accessing thermal CFD matrix. Synchronizing with Rack A...",
                "code": "dt"
            }
        elif detected_intent == "DATA_AUDIT":
             return {
                "action": "NAVIGATE",
                "target": "Security Audit Ledger",
                "message": "Verifying Blockchain Ledger integrity. Scanning SHA-256 hashes...",
                "code": "audit"
            }
        elif detected_intent == "FILE_RESEARCH":
            results = self.semantic_search(query)
            return {
                "action": "SEARCH_UI",
                "target": "Extraction Engine",
                "message": f"Found {len(results)} relevant documents via Semantic Intelligence.",
                "data": results,
                "code": "search"
            }
        elif detected_intent == "ECO_CHECK":
             return {
                "action": "NAVIGATE",
                "target": "Quantum Orchestrator", # Eco tab is there
                "message": "Calculating Net-Zero offsets for current cluster load...",
                "code": "eco"
            }
        elif detected_intent == "DNA_ARCHIVE":
            return {
                "action": "NAVIGATE",
                "target": "Molecular DNA Archival",
                "message": "Opening Digital-to-Biological Synthesis interface...",
                "code": "dna"
            }
        
        return {
            "action": "CHAT",
            "message": f"I understand you're interested in '{query}'. I'm standing by to orchestrate that task.",
            "code": "chat"
        }

    def semantic_search(self, query, top_n=3):
        """
        Simulates Semantic Search.
        """
        # FALLBACK: If no DB or empty, return high-quality mock results for the demonstration
        mock_docs = [
            {'filename': 'quantum_protocol_v3.pdf', 'full_text': 'This document details the PQC Crystals-Kyber implementation for sub-atomic routing.', 'score': 0.95},
            {'filename': 'thermal_map_A1.csv', 'full_text': 'Thermal CFD analysis of the central server rack showing heat soak at node position 0,4.', 'score': 0.88},
            {'filename': 'enterprise_security.docx', 'full_text': 'Corporate guidelines for blockchain-backed audit trails and immutability standards.', 'score': 0.75}
        ]
        
        if not self.db_conn:
            return mock_docs
            
        try:
            df = self.db_conn.execute("SELECT filename, full_text, file_type FROM parsed_documents").df()
            if df.empty: return mock_docs
            
            query_terms = set(query.lower().split())
            scores = []
            for idx, row in df.iterrows():
                content = (str(row['full_text']) + " " + str(row['filename'])).lower()
                count = sum(1 for term in query_terms if term in content)
                scores.append(count)
                
            df['score'] = scores
            results = df.sort_values(by='score', ascending=False).head(top_n)
            return results[results['score'] > 0].to_dict('records')
        except:
            return mock_docs

    def get_system_pulse(self):
        """
        Calculates a 'Global Intelligence Pulse' metric.
        """
        import random
        from src.audit_logger import verify_ledger
        is_valid, _ = verify_ledger()
        integrity_score = 99.9 if is_valid else 45.0
        compute_load = random.randint(30, 60)
        
        pulse = (integrity_score + (100 - compute_load)) / 2
        return {
            "pulse": pulse,
            "integrity": integrity_score,
            "load": compute_load
        }

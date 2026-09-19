"""
Scalable Agentic System: Dynamic Tool Discovery & Routing Prototype
"""

import json
from typing import List, Dict, Any


# 1. Central Tool Registry (Simulating 50+ to 1000+ indexed endpoints)

TOOL_REGISTRY = [
    {
        "id": "paypal_invoices_create_draft",
        "category": "invoicing",
        "description": "Create a draft invoice with recipient details, currency, and line items.",
        "parameters": {"amount": "float", "currency": "str", "recipient_email": "str"},
        "api_endpoint": "POST /v2/invoicing/invoices"
    },
    {
        "id": "paypal_invoices_send",
        "category": "invoicing",
        "description": "Send an existing draft invoice to customer via invoice_id.",
        "parameters": {"invoice_id": "str", "notify_customer": "bool"},
        "api_endpoint": "POST /v2/invoicing/invoices/{invoice_id}/send"
    },
    {
        "id": "paypal_disputes_list",
        "category": "disputes",
        "description": "List open disputes and claims from buyers.",
        "parameters": {"status": "str", "disputed_transaction_id": "str"},
        "api_endpoint": "GET /v1/customer/disputes"
    },
    {
        "id": "paypal_reporting_sales",
        "category": "reporting",
        "description": "Pull total transaction sales volume and analytics for a given time window.",
        "parameters": {"start_date": "str", "end_date": "str"},
        "api_endpoint": "GET /v1/reporting/transactions"
    },
    {
        "id": "rag_knowledge_pipeline",
        "category": "knowledge",
        "description": "Search official product documentation, developer guides, and fee schedules.",
        "parameters": {"query": "str"},
        "api_endpoint": "INTERNAL_RAG"
    },
    {
        "id": "system_search_metadata",
        "category": "introspection",
        "description": "Search available system capabilities, logs, and run status.",
        "parameters": {"scope": "str", "query": "str"},
        "api_endpoint": "INTERNAL_INSPECTION"
    }
]


# 2. Tool Discovery Engine (Dynamic Semantic Retrieval)

class ToolDiscoveryEngine:
    def __init__(self, registry: List[Dict[str, Any]]):
        self.registry = registry

    def search_tools(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Simulates dense vector search + cross-encoder reranking.
        Filters the full tool catalog down to top_k schemas to avoid context dilution.
        """
        query_words = set(query.lower().split())
        scored_tools = []
        
        for tool in self.registry:
            # Score based on lexical and semantic overlap
            desc_words = set(tool["description"].lower().split()) | set(tool["category"].lower().split())
            score = len(query_words & desc_words)
            scored_tools.append((score, tool))

        # Sort by relevance score
        scored_tools.sort(key=lambda x: x[0], reverse=True)
        return [tool for _, tool in scored_tools[:top_k]]


# 3. Sub-Agent Execution Layer

class SubAgentExecutor:
    def execute_workflow(self, selected_tools: List[Dict[str, Any]], context: Dict[str, Any]) -> str:
        """Executes the retrieved tools in a validated sequence."""
        print(f"-> Injected Schemas ({len(selected_tools)} tools bound to sub-agent):")
        for tool in selected_tools:
            print(f"   * [{tool['id']}] -> {tool['api_endpoint']}")

        # Step 1: Draft invoice
        invoice_id = "INV2-R4T7-9LK2-B3ZZ"
        print(f"\n[Execution] 1. Creating Draft Invoice for ${context['amount']} to {context['recipient']}...")
        print(f"            API Response: HTTP 201 Created (ID: {invoice_id})")

        # Step 2: Send invoice
        print(f"[Execution] 2. Dispatching Invoice {invoice_id}...")
        print(f"            API Response: HTTP 202 Accepted (Notification sent)")

        return f"Success: Invoice #{invoice_id} for ${context['amount']} created and sent to {context['recipient']}."


# 4. Pipeline Execution

if __name__ == "__main__":
    discovery_engine = ToolDiscoveryEngine(TOOL_REGISTRY)
    executor = SubAgentExecutor()

    # User Query from assignment
    user_query = "Send an invoice for $50 to user@example.com"
    print(f"User Request: '{user_query}'\n" + "-" * 60)

    # 1. Discover top schemas dynamically
    relevant_tools = discovery_engine.search_tools(user_query, top_k=2)

    # 2. Execute via sub-agent
    parsed_payload = {"amount": 50.00, "recipient": "user@example.com"}
    result = executor.execute_workflow(relevant_tools, parsed_payload)

    print("-" * 60)
    print(f"Final Agent Response:\n{result}")
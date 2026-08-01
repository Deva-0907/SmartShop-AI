import streamlit as st
from  agents.price_agent import PriceAgent
from agents.budget_agent import BudgetAgent
from agents.communication import AgentCommunicator


st.set_page_config(page_title="SmartShop AI", page_icon=" ", layout="wide")

st.title(" SmartShop AI")
st.caption(" 2-Agent Shopping & Budget Assistant")


@st.cache_resource
def init_agents():
    return {
        "price": PriceAgent(),
        "budget": BudgetAgent()
    }

agents = init_agents()


with st.sidebar:
    st.header(" Quick Stats")
    st.info(" **How it works:**\n\n"
            " **Price Agent** (Groq) finds products\n"
            " **Budget Agent** (OpenRouter) checks affordability\n"
            " Agents communicate automatically!")
    
    st.divider()
    st.caption(" Groq + OpenRouter")


if "messages" not in st.session_state:
    st.session_state.messages = []


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


if prompt := st.chat_input("Ask about prices or budgets..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    

    with st.chat_message("assistant"):
        with st.spinner(" Agents thinking..."):
            try:
                # STEP 1: Price Agent searches (Groq)
                price_result = agents["price"].search(prompt)
                
                # STEP 2: Price Agent → Budget Agent communication
                handoff = AgentCommunicator.process_handoff(price_result, prompt)
                
                # STEP 3: Budget Agent analyzes (OpenRouter)
                product_name = handoff["product_info"]["name"]
                budget_advice = agents["budget"].analyze(
                    prompt, 
                    product_name
                )
                

                final_response = f"""
**Price Agent found:**
{price_result['recommendation']}

** Budget Agent says:**
{budget_advice}

---
 *Price Agent uses Groq (fast) • Budget Agent uses OpenRouter (smart)*
                """
                
                st.markdown(final_response)
                st.session_state.messages.append({"role": "assistant", "content": final_response})
                
                # Show products in expander
                with st.expander("View all products found"):
                    for p in price_result["products"]:
                        st.write(f"- {p['name']}: **LKR {p['price']}** ({p['store']})")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Check your API keys in .env file")

st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔄 Reset Chat"):
        st.session_state.messages = []
        st.rerun()

    st.caption("Made with for Viva")